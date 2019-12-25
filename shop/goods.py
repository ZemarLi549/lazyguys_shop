#-*- coding:utf-8 -*-
# author:Administrator
# datetime:2019/8/12 13:26
# software: PyCharm
from django.shortcuts import HttpResponse as resp
from . import models
import json
import time


#处理查看细节按钮,更具ID查询点击商品的所有信息
from django.core import serializers
def collect_love(request):
    un = request.POST.get('un')
    goods_id = request.POST.get('goods_id')
    collect_status = request.POST.get('collect_status')
    if collect_status == 'true':
        add_time = time.strftime('%F %T')
        shuliang_add = models.UserFav.objects.filter(username=un,goods_id=goods_id).count()

        if not shuliang_add:
            models.UserFav.objects.create(username=un,
                                          goods_id=goods_id,
                                          add_time=add_time)
            goods_info = models.Goods.objects.filter(id=goods_id)[0]
            fav_num = goods_info.fav_num
            models.Goods.objects.filter(id=goods_id).update(fav_num=fav_num+1)
    else:
        shuliang_cancel = models.UserFav.objects.filter(username=un,goods_id=goods_id).count()
        if shuliang_cancel:
            models.UserFav.objects.filter(goods_id=goods_id,username=un).delete()
            goods_info = models.Goods.objects.filter(id=goods_id)[0]
            fav_num = goods_info.fav_num
            models.Goods.objects.filter(id=goods_id).update(fav_num=fav_num - 1)
    goods_info = models.Goods.objects.filter(id=goods_id)[0]
    fav_num = goods_info.fav_num
    msg = {"fav_num":fav_num}
    return resp(json.dumps(msg))
def viewdetails(request):
    goods_id = request.POST.get('goods_id')
    username = request.POST.get('username')
    if username:
        flag_collect = models.UserFav.objects.filter(username=username, goods_id=goods_id).count()
        if flag_collect:
            fav_flag = "YES"
        else:
            fav_flag = "NO"
    else:
        fav_flag = "NO"

    goods_info = models.Goods.objects.filter(id=goods_id)
    # 浏览量加一
    views_count_new = goods_info[0].views_count + 1
    models.Goods.objects.filter(id=goods_id).update(views_count=views_count_new)
    # 浏览量加一
    #按照参数栏给尺寸种类分
    parameter = goods_info[0].parameter
    size_type = json.loads(parameter)[2].strip('"')
    if ',' in size_type:
        size_type_list = size_type.split(',')
    else:
        size_type_list = size_type.split('款')
    color = json.loads(parameter)[3].strip('"')
    color_list = color.split('色')
    #按照参数栏给尺寸种类分
    json_goods_info = serializers.serialize("json", goods_info)
    json_goods_info = json.loads(json_goods_info)
    json_goods_info[0]['fields']['goods_img'] = json.loads(json_goods_info[0]['fields']['goods_img'])
    return resp(json.dumps({"json_goods_info": json_goods_info, "fav_flag": fav_flag,"size_type_list":size_type_list,"color_list":color_list}))


#处理查看细节按钮,更具ID查询点击商品的所有信息
