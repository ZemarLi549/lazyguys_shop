#-*- coding:utf-8 -*-
# author:Administrator
# datetime:2019/8/23 10:23
# software: PyCharm
from django.shortcuts import render,HttpResponse as resp
from . import models
import json
import random
import re
import os
import time
from django.core import serializers
from shop.views import to_json
from django.db.models import Q
def to_admin_index(request):
    if 'admin_info' in request.session.keys():
        re= models.Orders.objects.filter(Q(pay_status='货到付款发货中')|Q(pay_status='支付成功'))
        zongjia = 0.00
        sale_num=0
        men_sale_num = 0
        women_sale_num = 0
        children_sale_num = 0
        jingshouru=0.00
        men_jing = 0.00
        women_jing = 0.00
        children_jing = 0.00
        #获取当前月初的时间戳
        now_month = 0.00
        one_month = 0.00
        two_month = 0.00
        three_month = 0.00
        four_month = 0.00
        five_month = 0.00
        six_month = 0.00
        seven_month = 0.00
        now_month_num = 0
        one_month_num = 0
        two_month_num = 0
        three_month_num = 0
        four_month_num = 0
        five_month_num = 0
        six_month_num = 0
        seven_month_num = 0
        time_month_init = time.mktime(time.strptime(time.strftime('%Y-%m'), '%Y-%m'))
        time_month_one = time_month_init-30*24*3600
        time_month_two = time_month_one-30*24*3600
        time_month_three = time_month_two-30*24*3600
        time_month_four = time_month_three-30*24*3600
        time_month_five = time_month_four-30*24*3600
        time_month_six = time_month_five-30*24*3600
        time_month_seven = time_month_six-30*24*3600
        yi = time.strftime('%Y-%m', time.localtime(time_month_init))
        er = time.strftime('%Y-%m', time.localtime(time_month_one))
        san = time.strftime('%Y-%m', time.localtime(time_month_two))
        si = time.strftime('%Y-%m', time.localtime(time_month_three))
        wu = time.strftime('%Y-%m', time.localtime(time_month_four))
        liu = time.strftime('%Y-%m', time.localtime(time_month_five))
        qi = time.strftime('%Y-%m', time.localtime(time_month_six))
        ba = time.strftime('%Y-%m', time.localtime(time_month_seven))
        if re:
            for item in re:
                time_then = time.mktime( time.strptime(item.addtime, '%Y-%m-%d %H:%M:%S') )
                if time_then>time_month_init:
                    now_month_num = now_month_num+1#当前月订单量
                    now_month = now_month+float(item.total)#当前月的销售总额
                    now_month = round(now_month, 2)
                elif time_then>time_month_one and time_then<time_month_init:
                    one_month_num =one_month_num+1
                    one_month = one_month + float(item.total)#上2个月的销售总额
                    one_month = round(one_month, 2)
                elif time_then>time_month_two and time_then<time_month_one:
                    two_month_num = two_month_num+1
                    two_month = two_month + float(item.total)#上2个月的销售总额
                    two_month = round(two_month, 2)
                elif time_then>time_month_three and time_then<time_month_two:
                    three_month_num = three_month_num +1
                    three_month = three_month + float(item.total)#上3个月的销售总额
                    three_month = round(three_month, 2)
                elif time_then>time_month_four and time_then<time_month_three:
                    four_month_num = four_month_num+1
                    four_month = four_month + float(item.total)#上4个月的销售总额
                    four_month = round(four_month, 2)
                elif time_then>time_month_five and time_then<time_month_four:
                    five_month_num =five_month_num+1
                    five_month = five_month + float(item.total)#上5个月的销售总额
                    five_month = round(five_month, 2)
                elif time_then>time_month_six and time_then<time_month_five:
                    six_month_num = six_month_num +1
                    six_month = six_month + float(item.total)#上6个月的销售总额
                    six_month = round(six_month, 2)
                elif time_then>time_month_seven and time_then<time_month_six:
                    seven_month_num = seven_month_num+1
                    seven_month = seven_month + float(item.total)#上7个月的销售总额
                    seven_month = round(seven_month,2)
                zongjia = zongjia+float(item.total)#销售总额
                zongjia = round(zongjia,2)
                goods_info = json.loads(item.goods_info)
                for good in goods_info:
                    if good['category_yi']=='women':
                        women_sale_num = women_sale_num+int(good['goods_num'])
                        women_jing = women_jing+int(good['goods_num'])*float(good['lirun'])
                    elif good['category_yi']=='men':
                        men_sale_num =men_sale_num+int(good['goods_num'])
                        men_jing = men_jing + int(good['goods_num']) * float(good['lirun'])
                    else:
                        children_sale_num = children_sale_num+int(good['goods_num'])
                        children_jing = children_jing + int(good['goods_num']) * float(good['lirun'])
                    sale_num = sale_num+int(good['goods_num'])#总销售量
                    jingshouru = float(good['lirun'])*int(good['goods_num'])+jingshouru
                pass
        products_num = models.Goods.objects.all().count()
        all_users = models.User.objects.all()
        all_users_plus = []
        for user in all_users:
            total = 0.00
            user_orders = models.Orders.objects.filter(username=user.username)
            for order in user_orders:
                total = total+float(order.total)
            dic = {"username":user.username,
                   "nickname":user.nickname,
                   "info":user.info,
                   "email":user.email,
                   "birthday":user.birthday,
                   "total":total}
            all_users_plus.append(dic)#按照用户总消费额排序
        all_users_plus.sort(key=lambda item:item['total'],reverse=True)
        return render(request,'adminpage/index.html',{"all_users":all_users_plus,"zongjia":zongjia,"sale_num":sale_num,"products_num":products_num,"jingshouru":jingshouru,
                                                      "fenxiao_num":{"women_sale_num":women_sale_num,"men_sale_num":men_sale_num,"children_sale_num":children_sale_num},
                                                      "fenxiao_lirun":{"women_jing":women_jing,"men_jing":men_jing,"children_jing":children_jing},
                                                      "qianba_sale":{"yi":now_month,"er":one_month,"san":two_month,"si":three_month,"wu":four_month,"liu":five_month,"qi":six_month,"ba":seven_month,
                                                                     "mon_yi":yi,"mon_er":er,"mon_san":san,"mon_si":si,"mon_wu":wu,"mon_liu":liu,"mon_qi":qi,"mon_ba":ba,
                                                                     "yi_month_num":now_month_num,"er_month_num":one_month_num,"san_month_num":two_month_num,"si_month_num":three_month_num,
                                                                     "wu_month_num":four_month_num,"liu_month_num":five_month_num,"qi_month_num":six_month_num,"ba_month_num":seven_month_num,}})

    else:
        return render(request,'404.html')


def loginverify(request):
    mg = request.POST.get('manager')
    pw = request.POST.get('password')
    if mg:
        mg_exist = models.Admin.objects.filter(manager=mg)
        if mg_exist:
            mg_pw = models.Admin.objects.filter(manager=mg,password=pw)
            if mg_pw:
                msg = {'status': True}
                request.session['admin_info'] = {"admin_name":mg,"admin_psw":pw}
                pass
            else:
                msg = {'status': False, 'Tip': '密码输入错误!!'}
        else:
            msg = {'status': False, 'Tip': '该用户不属于管理员!!'}


    else:
        msg = {'status': False, 'Tip': '请输入用户名!'}

    return resp(json.dumps(msg))

def to_manage_page(request):
    return render(request,'shop_houtaidenglu_index.html')


def to_modify_goods(request):
    product_list = models.Goods.objects.all()
    product_list = to_json(product_list)
    return render(request,'adminpage/modify_goods.html',{"product_list":product_list})
def to_modify_item(request):
    goods_id = request.GET.get('goods_id')
    goods_info = models.Goods.objects.filter(id=goods_id)
    # 评论初始化显示
    reviews_list = models.Comments.objects.filter(goods_id=goods_id).order_by('-cmts_star')
    # 评论初始化显示
    # 初始显示所有问答
    wenda_list = models.AskForm.objects.filter(goods_id=goods_id).order_by('-dianzan')
    wenda_list = serializers.serialize('json', wenda_list)
    wenda_list = json.loads(wenda_list)
    if wenda_list:
        for item in wenda_list:
            item['fields']['da'] = json.loads(item['fields']['da'])
    # 初始显示所有问答
    # 按照参数栏给尺寸种类分
    parameter = goods_info[0].parameter
    size_type = json.loads(parameter)[2].strip('"')
    size_type_list = size_type.split('款')
    color = json.loads(parameter)[3].strip('"')
    color_list = color.split('色')
    # 按照参数栏给尺寸种类分
    #查找收藏此商品的用户
    users_fav_list=[]
    users_fav = models.UserFav.objects.filter(goods_id=goods_id)
    for user in users_fav:
        username = user.username
        re = models.User.objects.filter(username=username)
        if re:
            dic = {"username":username,
                   "nickname":re[0].nickname,
                   "email":re[0].email,
                   "birthday":re[0].birthday,
                   "info":re[0].info}
            users_fav_list.append(dic)
    #查找收藏此商品的用户
    #查找添加此商品为购物车的用户
    users_cart_list = []
    users_cart = models.Cart.objects.filter(goods_id=goods_id)
    for user in users_cart:
        username = user.username
        result = models.User.objects.filter(username=username)
        if result:
            dic_cart = {"username":username,
                   "nickname":result[0].nickname,
                   "email":result[0].email,
                   "birthday":result[0].birthday,
                   "info":result[0].info}
            users_cart_list.append(dic_cart)
    #查找添加此商品为购物车的用户
    json_goods_info = to_json(goods_info)
    return render(request,'adminpage/modify_item.html',{"goods_info":json_goods_info[0],"reviews_list":reviews_list,"size_type_list":size_type_list,"color_list":color_list,"wenda_list":wenda_list,"users_cart":users_cart_list,"users_fav":users_fav_list})

def ajax_sort_houtai(request):
    ajax_list = models.Goods.objects.all()
    ajax_list = to_json(ajax_list)
    search_again_cont_pre = request.POST.get('search_again_cont')
    search_again_cont = search_again_cont_pre.replace(' ', '')  # 去掉空字符
    ajax_list_search = []
    pattern = r'' + search_again_cont + '.+'
    for item in ajax_list:
        str_search = item['fields']['goods_brief'] + item['fields']['name'] + item['fields']['goods_desc'] + str(item['fields']['parameter'])
        if re.search(pattern, str_search, re.I):  # 如果存在搜索内容的话
            ajax_list_search.append(item)
        pass
    pass
    random.shuffle(ajax_list_search)
    ajax_list = ajax_list_search
    return resp(json.dumps({"ajax_list":ajax_list}))
def create_tu(tu1,hide_id,goods_img_list,num):
    if tu1:#修改了主图
        ext = os.path.splitext(tu1.name)[1]
        tu_name = str(time.time()*1000)[:13]+hide_id+str(num)+ext
        with open(os.path.join('StaticResources/goods/update_imgs/'+tu_name),'wb') as f:
            for chunk in tu1.chunks(chunk_size = 1024):
                f.write(chunk)
                pass
        tu_one = '/static/goods/update_imgs/'+tu_name
        last_img = goods_img_list[num]
        index_gang = last_img.rfind('/')
        last_img = last_img[index_gang+1:]
        flag_remove = os.path.splitext(last_img)[0]
        if flag_remove.isdigit():
            os.remove(os.path.join('StaticResources/goods/update_imgs/'+last_img))
    else:
        tu_one = goods_img_list[num]
        pass
    return tu_one
def modify_good_info(request):#修改到这了
    tu1 = request.FILES.get('tu1')
    tu2 = request.FILES.get('tu2')
    tu3 = request.FILES.get('tu3')
    hide_id = request.POST.get('hide_id')
    goods_img_list = json.loads(models.Goods.objects.filter(id=hide_id)[0].goods_img)
    tu_one = create_tu(tu1,hide_id,goods_img_list,0)
    tu_two = create_tu(tu2,hide_id,goods_img_list,1)
    tu_three = create_tu(tu3,hide_id,goods_img_list,2)
    goods_img = json.dumps([tu_one,tu_two,tu_three])
    name = request.POST.get('name')
    original_price = request.POST.get('original_price')
    current_price = request.POST.get('current_price')
    goods_stock = request.POST.get('goods_stock')
    fav_num = request.POST.get('fav_num')
    views_count = request.POST.get('views_count')
    goods_brief = request.POST.get('goods_brief')
    goods_desc = request.POST.get('goods_desc')
    sale_count = request.POST.get('sale_count')
    haoping = request.POST.get('haoping')
    lirun = request.POST.get('lirun')
    is_new = request.POST.get('is_new')
    parameter1 = request.POST.get('parameter1')
    parameter2 = request.POST.get('parameter2')
    parameter3 = request.POST.get('parameter3')
    parameter4 = request.POST.get('parameter4')
    parameter5 = request.POST.get('parameter5')
    parameter_list = [parameter1,parameter2,parameter3,parameter4,parameter5]
    parameter = json.dumps(parameter_list)
    category_yi = request.POST.get('category_yi')
    category_er = request.POST.get('category_er')
    category_san = request.POST.get('category_san')
    category_si = request.POST.get('category_si')
    is_sale = request.POST.get('is_sale')
    models.Goods.objects.filter(id=hide_id).update(name=name,
                                                   original_price=original_price,
                                                   current_price=current_price,
                                                   goods_stock=goods_stock,
                                                   category_yi=category_yi,
                                                   category_er=category_er,
                                                   category_san=category_san,
                                                   category_si=category_si,
                                                   fav_num=fav_num,
                                                   views_count=views_count,
                                                   sale_count=sale_count,
                                                   goods_brief=goods_brief,
                                                   goods_img=goods_img,
                                                   goods_desc=goods_desc,
                                                   is_sale=is_sale,
                                                   is_new=is_new,
                                                   haoping=haoping,
                                                   lirun=lirun,
                                                   parameter=parameter)
    return resp(json.dumps({"status":True}))
def del_good(request):
    goods_id = request.POST.get('goods_id')
    models.Goods.objects.filter(id=goods_id).delete()
    return resp(json.dumps({"status":True}))
def add_good(request):
    models.Goods.objects.create(name='这里填商品名称',
                                goods_stock=88,
                                category_yi='women',
                                goods_brief='这是商品的简介',
                                goods_desc='这是商品的阐述,确保用户能搜索关键字',
                                goods_img=json.dumps(["/static/MetronicShopUI/assets/LoginImg/lan.jpg","/static/MetronicShopUI/assets/LoginImg/lan.jpg","/static/MetronicShopUI/assets/LoginImg/lan.jpg"]))
    return resp(json.dumps({"status":True}))
def del_wenda(request):
    ask_id = request.POST.get('ask_id')
    re = models.AskForm.objects.filter(id=ask_id)
    if re:
        models.AskForm.objects.filter(id=ask_id).delete()
        msg={"status":True}
    else:
        msg={"status":False}
    return resp(json.dumps(msg))
def del_review(request):
    review_id = request.POST.get('review_id')
    re = models.Comments.objects.filter(cmts_id=review_id)
    if re:
        models.Comments.objects.filter(cmts_id=review_id).delete()
        msg={"status":True}
    else:
        msg={"status":False}
    return resp(json.dumps(msg))
def to_order_center(request):
    order_list=models.Orders.objects.all()
    json_order_list = serializers.serialize("json", order_list)
    order_list = json.loads(json_order_list)
    if order_list:
        for item in order_list:
            item['fields']['goods_info'] = json.loads(item['fields']['goods_info'])
    return render(request, 'adminpage/order_center.html', {"order_list": order_list})
def toadministrator(request):
    return render(request,'adminpage/shop_houtaidenglu_wanglei.html')