#-*- coding:utf-8 -*-
# author:Administrator
# datetime:2019/8/12 13:26
# software: PyCharm
from django.shortcuts import render,HttpResponse as resp
from . import models
from shop.views import to_json    #必须这么写才行
import json
import random
from django.db.models import Q

def to_collect(request):
    user = request.session['user_info']
    username = user['username']
    un = models.UserFav.objects.filter(username=username)
    goods_list = []
    for item in un:
        goods_list.append(item.goods_id)
    product_list = models.Goods.objects.filter(id__in=goods_list)
    product_list = to_json(product_list)
    return render(request,'shop-wishlist.html',{"product_list":product_list})

#从数据库查找出登录人的收藏列表


#收藏商品的移出数据库
def remove_collect(request):
    goods_id = request.POST.get('get_goods_id')
    user = request.session['user_info']
    username = user['username']
    # print(goods_id,username)
    models.UserFav.objects.filter(goods_id = goods_id,username = username).delete()
    goods_info = models.Goods.objects.filter(id=goods_id)[0]
    fav_num = goods_info.fav_num
    models.Goods.objects.filter(id=goods_id).update(fav_num=fav_num - 1)#减少该商品的收藏量-1
    return resp(json.dumps({"status":True}))
def cart_manage(request):
    cart_goods_info = request.POST.get('good_info')
    user = request.session['user_info']
    username = user['username']
    cart_goods_info = json.loads(cart_goods_info)
    models.Cart.objects.create(username=username,
                               goods_id=cart_goods_info['goods_id'],
                               goods_size = cart_goods_info['goods_size'],
                               goods_img = cart_goods_info['goods_img'],
                               goods_name =cart_goods_info['goods_name'],
                               goods_totalprice = cart_goods_info['goods_totalprice'],#字符串也能存进decimal
                               goods_stock = cart_goods_info['goods_stock'],
                               goods_unitprice = cart_goods_info['goods_unitprice'],
                               goods_color = cart_goods_info['goods_color'],
                               number = cart_goods_info['goods_num'],
                               )
    return resp(json.dumps({"status":True}))
def del_cart_good(request):
    goods_id = request.POST.get('goods_id')
    goods_color = request.POST.get('goods_color')
    goods_size = request.POST.get('goods_size')
    user = request.session['user_info']
    username = user['username']
    # print(username,goods_id,goods_color,goods_size)
    models.Cart.objects.filter(username=username,goods_id=goods_id,goods_color=goods_color,goods_size=goods_size).delete()
    return resp(json.dumps({"status":True}))
def to_my_cart(request):
    user = request.session['user_info']
    username = user['username']
    cart_goods = models.Cart.objects.filter(username=username)
    zonjia = 0.00
    biaoqian_list = []#定义空列表装商品标签名称
    goods_id_list = []#定义空列表装商品标签名称
    if cart_goods:
        for item in cart_goods:
            biaoqian_list.append(item.goods_name)
            goods_id_list.append(item.goods_id)
            # print(float(item.goods_totalprice))
            zonjia = zonjia + float(item.goods_totalprice)
    zonjia = float('%.2f' % zonjia)
    tuijian_list = models.Goods.objects.filter(( ~Q(id__in=goods_id_list) ) & Q(name__in=biaoqian_list))
    tuijian_list = to_json( tuijian_list[:8] )
    random.shuffle(tuijian_list)
    return render(request,'my_cart.html',{"cart_goods":cart_goods,"zongjia":zonjia,"tuijian_list":tuijian_list})
def to_myshippingaddress(request):
    user = request.session['user_info']
    username = user['username']
    address_list = models.UserAddress.objects.filter(username=username)
    return render(request,'my_shipping_address.html',{"address_list":address_list})
def del_address(request):
    user = request.session['user_info']
    username = user['username']
    dizhiid = request.POST.get('dizhiid')
    models.UserAddress.objects.filter(username=username,id=dizhiid).delete()
    return resp(json.dumps({"status":True}))
def add_shippingaddr(request):
    user = request.session['user_info']
    username = user['username']
    signer_name = request.POST.get('signer_name')
    signer_mobile = request.POST.get('signer_mobile')
    province = request.POST.get('province')
    city = request.POST.get('city')
    district = request.POST.get('district')
    address = request.POST.get('address')
    if username and signer_name and signer_mobile and province and city and district and address:
        models.UserAddress.objects.create(username=username,  # 当填写完整后自动保存到个人收货地址信息中
                                          signer_name=signer_name,
                                          signer_mobile=signer_mobile,
                                          province=province,
                                          city=city,
                                          district=district,
                                          address=address,
                                          )
    return resp(json.dumps({"status":True}))