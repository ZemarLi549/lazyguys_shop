#-*- coding:utf-8 -*-
# author:Administrator
# datetime:2019/8/12 13:27
# software: PyCharm
from django.shortcuts import render,HttpResponse as resp,redirect
from . import models
import json
import time
from django.core import serializers
def to_shop_cart(request):
    return render(request,'shop-shopping-cart.html')
def to_checkout(request):
    user = request.session['user_info']
    username = user['username']
    address_list = models.UserAddress.objects.filter(username=username)#获取常用地址列表

    cart_goods = request.session['cart_goods']
    zonjia = 0.00
    if cart_goods:
        for item in cart_goods:
            zonjia = zonjia+float(item['goods_totalprice'])
    zonjia = float('%.2f' %zonjia)
    # print('嘿嘿黑', cart_goods,'总价',zonjia)
    return  render(request,'shop-checkout.html',{"cart_goods":cart_goods,"zongjia":zonjia,"address_list":address_list})
def checkout_init(request):
    cart_goods = request.POST.get('cart_goods')#购物车页面上的cartgoods
    re_list = json.loads(cart_goods)
    msg = {'status': True}
    for good in re_list:#后台管理需要加上一级分类和利润信息再加上二级分类吧可能后期需要
        goods_id = good['goods_id']
        re = models.Goods.objects.filter(id=goods_id)
        if re:
            category_yi = re[0].category_yi
            category_er = re[0].category_er
            lirun = re[0].lirun
            good['category_yi'] = category_yi
            good['category_er'] = category_er
            good['lirun'] = str(lirun)
        else:
            tips = good['goods_name']+'商品已被删除!'
            msg = {"status":False,"tips":tips}
    request.session['cart_goods'] = re_list
    # print('哈哈哈',cart_goods)
    return  resp(json.dumps(msg))
from shop.alipay import AliPay
import os
def order_execute(request):#记录收货地址等信息,创建订单入数据库
    user = request.session['user_info']
    username = user['username']
    signer_name = request.POST.get('name-dd')
    signer_mobile = request.POST.get('telephone-dd')
    province = request.POST.get('province')
    city = request.POST.get('city')
    district = request.POST.get('town')
    address = request.POST.get('add_detail')
    shiptype = str(request.POST.getlist('FlatShippingRate'))#得用getlist获取多个选项,str转换
    append_desc = request.POST.get('append_desc')
    append_pay_desc = request.POST.get('delivery-payment-method')
    #order字段
    remark = "本订单快递方式:"+shiptype+",用户附加说明:"+append_desc+","+append_pay_desc
    receive_address = province+city+district+address
    receive_name = signer_name
    pay_type = request.POST.get('CashOnDelivery')
    receive_tel = signer_mobile
    order_num = str(time.time() * 10000)[:14] + username[-4:]#命名方式时间戳加手机号后四位
    goods_info = request.session['cart_goods'] #进入结算页面会生成缓存商品信息在这里引用

    zonjia = 0.00
    for item in goods_info:
        zonjia = zonjia + float(item['goods_totalprice'])
    total = float('%.2f' % zonjia)
    if pay_type=='货到付款':
        pay_status="货到付款发货中"
        msg = {"status": False}
    elif pay_type=='支付宝支付':
        pay_status = "待支付"
        print('支付宝支付!')
        alipay = AliPay(
            appid="2016101200668181",
            app_notify_url="http://127.0.0.1:8000/alipay_return_notify",
            app_private_key_path=os.path.join("StaticResources/trade/keys/private_2048.txt"),
            alipay_public_key_path=os.path.join("StaticResources/trade/keys/alipay_key_2048.txt"),  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥),
            debug=True,  # 默认False,
            return_url="http://127.0.0.1:8000/alipay_return_url"
        )
        url = alipay.direct_pay(
            subject=username+"用户的订单",
            out_trade_no=order_num,
            total_amount=total,
        )
        re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)
        print('支付宝url',re_url)
        msg = {"status":True,"re_url":re_url}
    else:
        pay_status = "待支付"
        msg = {"status": False}
    request.session['order'] = {"username":username,
                                "order_num":order_num,
                                "goods_info":goods_info,
                                "total":total,
                                "receive_name":receive_name,
                                "receive_address":receive_address,
                                "receive_tel":receive_tel,
                                "addtime":time.strftime('%F %T'),
                                "remark":remark,
                                "pay_type":pay_type,
                                "pay_status":pay_status,
                                }#此次订单存session,离开支付页面删除此缓存
    models.Orders.objects.create(username=username,
                                order_num=order_num,
                                goods_info=json.dumps(goods_info),#存入数据库必须是字符串格式
                                total=total,
                                receive_name=receive_name,
                                receive_address=receive_address,
                                receive_tel=receive_tel,
                                addtime=time.strftime('%F %T'),
                                remark=remark,
                                pay_type=pay_type,
                                pay_status=pay_status,)
    # order
    if username and signer_name and signer_mobile and province and city and district and address:
        add_flag = models.UserAddress.objects.filter(username=username,signer_name=signer_name)
        if not add_flag:#如果此用户此次填写的收货人不是库里的话就新建一个新收获地址,否则不添加库了
            models.UserAddress.objects.create(username=username,#当填写完整后自动保存到个人收货地址信息中
                                              signer_name=signer_name,
                                              signer_mobile=signer_mobile,
                                              province=province,
                                              city=city,
                                              district=district,
                                              address=address,
                                              )

    #订单受理发消息
    content_order = '尊敬的'+username+'客户'+',您的订单'+order_num+'已受理!'
    models.Chat.objects.create(content=content_order,
                               send='18713585378',
                               receive=username,
                               time = time.strftime('%F %T'))
    #订单受理发消息
    return resp(json.dumps(msg))
def alipay_return_notify(request):
    """
    处理支付宝的notify_url
    :param request:
    :return:
    """
    processed_dict = {}
    for key, value in request.POST.items():
        processed_dict[key] = value
    print('之前的',processed_dict)
    sign = processed_dict.pop("sign", None)
    alipay = AliPay(
        appid="2016101200668181",
        app_notify_url="http://127.0.0.1:8000/alipay_return_notify",
        app_private_key_path=os.path.join("StaticResources/trade/keys/private_2048.txt"),
        alipay_public_key_path=os.path.join("StaticResources/trade/keys/alipay_key_2048.txt"),
        # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥),
        debug=True,  # 默认False,
        return_url="http://127.0.0.1:8000/alipay_return_url"
    )

    verify_re = alipay.verify(processed_dict, sign)

    if verify_re is True:
        print(processed_dict)
        # order_sn = processed_dict.get('out_trade_no', None)
        trade_no = processed_dict.get('out_trade_no', None)
        trade_status = processed_dict.get('trade_status', None)
        print(trade_status)
        if trade_status=='TRADE_SUCCESS':
            pay_status = '支付成功'
        elif trade_status=='TRADE_CLOSED':
            pay_status = '超时关闭'
        elif trade_status=='TRADE_FINISHED':
            pay_status = '交易结束,若想退款请联系管理员'
        elif trade_status=='WAIT_BUYER_PAY':
            pay_status = '待支付'
        else:
            pay_status = '待支付'
        models.Orders.objects.filter(order_num=trade_no).update(pay_status=pay_status,addtime=time.strftime('%F %T'),)
        print('支付宝notify创建成功!')
        return resp('success')
    pass

def alipay_return_url(request):
    """
    处理支付宝的return_url返回
    :param request:
    :return:
    """
    processed_dict = {}
    for key, value in request.GET.items():
        processed_dict[key] = value

    sign = processed_dict.pop("sign", None)

    alipay = AliPay(
        appid="2016101200668181",
        app_notify_url="http://127.0.0.1:8000/alipay_return_notify",
        app_private_key_path=os.path.join("StaticResources/trade/keys/private_2048.txt"),
        alipay_public_key_path=os.path.join("StaticResources/trade/keys/alipay_key_2048.txt"),
        # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥),
        debug=True,  # 默认False,
        return_url="http://127.0.0.1:8000/alipay_return_url"
    )

    verify_re = alipay.verify(processed_dict, sign)
    print(verify_re)
    if verify_re is True:
        # order_sn = processed_dict.get('trade_no', None)
        trade_no = processed_dict.get('out_trade_no', None)
        pay_status = '支付成功'
        models.Orders.objects.filter(order_num=trade_no).update(pay_status=pay_status,addtime=time.strftime('%F %T'),)
        return redirect('/to_myorder')
    else:
        return resp('<h1>您已进入防火墙,退下吧!</h1>')
def to_alipay_page(request):
    username = request.session['user_info']['username']
    order_num = request.POST.get('order_num')
    total = request.POST.get('total')
    alipay = AliPay(
        appid="2016101200668181",
        app_notify_url="http://127.0.0.1:8000/alipay_return_notify",
        app_private_key_path=os.path.join("StaticResources/trade/keys/private_2048.txt"),
        alipay_public_key_path=os.path.join("StaticResources/trade/keys/alipay_key_2048.txt"),
        # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥),
        debug=True,  # 默认False,
        return_url="http://127.0.0.1:8000/alipay_return_url"
    )
    url = alipay.direct_pay(
        subject=username + "用户的订单",
        out_trade_no=order_num,
        total_amount=total,
    )
    re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)
    msg = {"status": True, "re_url": re_url}
    return resp(json.dumps(msg))
def to_pay_page(request):#创建订单了进入支付页面
    order = request.session['order']
    # print(order)
    #销售量加num,订单中不止一个商品需要循环获取
    if order:
        for item in order['goods_info']:
            goods_id = int(item['goods_id'])
            goods_num = int(item['goods_num'])
            sale_count_new = models.Goods.objects.filter(id=goods_id)[0].sale_count+goods_num
            goods_stock_new = models.Goods.objects.filter(id=goods_id)[0].goods_stock-goods_num
            models.Goods.objects.filter(id=goods_id).update(sale_count=sale_count_new)
            models.Goods.objects.filter(id=goods_id).update(goods_stock=goods_stock_new)
    #销售量加num,库存减num
    return render(request,'pay_page.html',{"order":order})
def change_paystatus(request):#模拟支付成功后期删除
    user = request.session['user_info']
    username = user['username']
    dingdanhao = request.POST.get('dingdanhao')
    models.Orders.objects.filter(username=username,order_num=dingdanhao).update(pay_status='支付成功')
    return resp(json.dumps({"status":True}))
def to_myorder(request):#到自己的订单页面
    user = request.session['user_info']
    username = user['username']
    order_list = models.Orders.objects.filter(username=username)
    json_order_list = serializers.serialize("json", order_list)
    order_list = json.loads(json_order_list)
    if order_list:
        for item in order_list:
            item['fields']['goods_info'] = json.loads(item['fields']['goods_info'])
    return render(request,'my_order.html',{"order_list":order_list})
def del_order(request):#用户删除自己的订单修改username后加del,用户搜不到,但是管理员得有
    user = request.session['user_info']
    username = user['username']
    order_num = request.POST.get('order_num')
    models.Orders.objects.filter(username=username,order_num=order_num).update(username=username+'del')
    return resp(json.dumps({"status":True}))