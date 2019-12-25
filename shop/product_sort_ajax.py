#-*- coding:utf-8 -*-
# author:Administrator
# datetime:2019/8/19 13:22
# software: PyCharm
from django.shortcuts import render,HttpResponse as resp
from . import models
import json
import random
import math
from django.core.paginator import Paginator
import re
from shop.views import to_json
from django.db.models import Q
def to_ajax_list(ajax_list,sort_type,range_click,price_range):
    pattern = r'\d+'
    if range_click == 'YES':  # 通过点击区间按钮进入的后台
        min = float(re.findall(pattern, price_range)[0])
        max = float(re.findall(pattern, price_range)[1])
        ajax_list_range = []
        for item in ajax_list:
            if float(item['fields']['current_price']) >= min and float(item['fields']['current_price']) <= max:
                ajax_list_range.append(item)
                pass
            pass
        ajax_list = ajax_list_range

        pass
    else:  # 通过输入框值变换进入的后台
        if sort_type == '价格从高到低':  # lambda后需要转换成float,或者int
            ajax_list.sort(key=lambda item: (float(item['fields']['current_price'])), reverse=True)
        elif sort_type == '价格从低到高':
            ajax_list.sort(key=lambda item: (float(item['fields']['current_price'])))
        elif sort_type == '按销售量':
            ajax_list.sort(key=lambda item: (int(item['fields']['sale_count'])), reverse=True)
        elif sort_type == '按好评量':
            ajax_list.sort(key=lambda item: (int(item['fields']['haoping'])), reverse=True)
        elif sort_type == '按浏览量':
            ajax_list.sort(key=lambda item: (int(item['fields']['views_count'])), reverse=True)
        elif sort_type == '热卖':
            ajax_list_sale = []
            for item in ajax_list:
                if item['fields']['is_sale'] == True:
                    ajax_list_sale.append(item)
                pass
            random.shuffle(ajax_list_sale)  # 随机排序,没有返回值!不能赋值
            ajax_list = ajax_list_sale
        elif sort_type == '新品':
            ajax_list_new = []
            for item in ajax_list:
                if item['fields']['is_new'] == True:
                    ajax_list_new.append(item)
                pass
            random.shuffle(ajax_list_new)
            ajax_list = ajax_list_new
        else:
            random.shuffle(ajax_list)
    return ajax_list
def ajax_sort(request):
    sort_type = request.POST.get('sort_type')
    range_click = request.POST.get('range_click')
    price_range = request.POST.get('price_range')
    # print('这个是sort之前页面', request.session['product_list']['product_list'])
    ajax_list = request.session['product_list']['product_list']
    ajax_list = to_ajax_list(ajax_list,sort_type,range_click,price_range)
    # print('这个是sort之后页面', ajax_list)
    request.session['product_list_page'] = {"product_list": ajax_list}  # 改session的值,以便于分页
    count = len(ajax_list)
    item = 9
    all_pages = math.ceil(count / item)
    all_page_list = [i + 1 for i in range(all_pages)]
    product_list_page = ajax_list[:9]
    return resp(json.dumps({"ajax_list":product_list_page,"all_page_list":all_page_list}))


def to_search_result(request):
    search_content_pre = request.POST.get('search_content')
    if search_content_pre:
        search_content = search_content_pre.replace(' ','')#去掉空字符
        product_list_search = models.Goods.objects.filter(Q(goods_brief__icontains=search_content) | Q(goods_desc__icontains=search_content) | Q(name__icontains=search_content) | Q(parameter__icontains=search_content))
        product_list_search = to_json(product_list_search)
        #搜索关键字存库
        keywords_list = models.HotSearchWords.objects.filter(keywords=search_content)
        if keywords_list:#若果存在才会加一
            index_new = keywords_list[0].index+1
            models.HotSearchWords.objects.filter(keywords=keywords_list[0].keywords).update(index=index_new)
        if len(keywords_list) == 0:
            models.HotSearchWords.objects.create(keywords=search_content)
        #搜索关键字存库
    else:
        search_content_pre = '热搜'
        product_list_search = models.Goods.objects.all().order_by('-views_count')[:50]
        product_list_search = to_json(product_list_search)

    # 畅销前四商品本页面并且是sale或者new的
    # print('到list页面', product_list)
    relative_sale_list = []  # 为你推荐
    for item in product_list_search:
        if item['fields']['is_sale'] == True or item['fields']['is_new'] == True:
            relative_sale_list.append(item)
    relative_sale_list.sort(key=lambda item: (int(item['fields']['sale_count'])), reverse=True)
    relative_sale_list = relative_sale_list[:10]
    random.shuffle(relative_sale_list)
    relative_sale_list = relative_sale_list[:4]  # 随机展示前10的4哥产品
    # 畅销前四商品本页面


    request.session['product_list_search']=product_list_search
    request.session['product_list_search_page'] = product_list_search  # 缓存分类后用分页
    # 分页
    count = len(product_list_search)
    item = 9
    all_pages = math.ceil(count / item)
    all_page_list = [i + 1 for i in range(all_pages)]
    product_list_page = product_list_search[:9]
    # 分页
    # print(request.session['product_list_search'])
    return render(request,'shop-search-result.html',{"product_list":product_list_page,"all_page_list":all_page_list,"search_content_pre":search_content_pre,"relative_sale_list":relative_sale_list})
def ajax_sort_search(request):
    search_again_click = request.POST.get('search_again_click')
    # print('这个是sort之前页面', request.session['product_list']['product_list'])
    if search_again_click == 'YES':#筛选条件是再搜索的
        ajax_list = request.session['product_list_search']
        search_again_cont_pre = request.POST.get('search_again_cont')
        search_again_cont = search_again_cont_pre.replace(' ', '')  # 去掉空字符
        ajax_list_search = []
        pattern = r'' + search_again_cont + '.+'
        for item in ajax_list:
            str_search = item['fields']['goods_brief']+item['fields']['name']+item['fields']['goods_desc']+str(item['fields']['parameter'])
            if re.search(pattern,str_search,re.I):#如果存在搜索内容的话
                ajax_list_search.append(item)
            pass
        pass
        random.shuffle(ajax_list_search)
        ajax_list = ajax_list_search
    else:#筛选条件不是再搜索的
        ajax_list = request.session['product_list_search']
        sort_type = request.POST.get('sort_type')
        range_click = request.POST.get('range_click')
        price_range = request.POST.get('price_range')
        ajax_list = to_ajax_list(ajax_list,sort_type,range_click,price_range)
    request.session['product_list_search_page'] = ajax_list  # 改session的值,以便于分页
    count = len(ajax_list)
    item = 9
    all_pages = math.ceil(count / item)
    all_page_list = [i + 1 for i in range(all_pages)]
    product_list_page = ajax_list[:9]
    return resp(json.dumps({"ajax_list":product_list_page,"all_page_list":all_page_list}))

def search_tips(request):
    search_content = request.POST.get('search_content')
    search_list = models.HotSearchWords.objects.filter(keywords__icontains=search_content)[:6]#只给6个提示栏
    tips_list = []
    for item in search_list:
        dic = {}
        dic["keywords"] = item.keywords
        tips_list.append(dic)
    return resp(json.dumps(tips_list))
def page_display(request):
    # 分页
    product_list = request.session['product_list_page']['product_list']
    page_num = request.GET.get('page_num')
    if not page_num:
        page_num = 1
    elif not page_num.isdigit():
        page_num = 2#如果按下下一页时候(初始定义)

    page_num = int(page_num)
    count = len(product_list)
    item = 9
    all_pages = math.ceil(count/item)
    all_page_list = [i + 1 for i in range(all_pages)]
    product_list_page = Paginator(product_list, item).page(page_num)
    product_list_json = {"object_list":product_list_page.object_list,
                         "number":product_list_page.number,
                         }#要转换成json,分页后是一个结果集合序列化不了,只能循环赋值

    return resp(json.dumps({"product_list_json":product_list_json,"all_page_list":all_page_list}))
    # 分页
def page_display_search(request):
    # 分页
    product_list = request.session['product_list_search_page']
    page_num = request.GET.get('page_num')
    if not page_num:
        page_num = 1
    elif not page_num.isdigit():
        page_num = 2#如果按下下一页时候(初始定义)

    page_num = int(page_num)
    count = len(product_list)
    item = 9
    all_pages = math.ceil(count/item)
    all_page_list = [i + 1 for i in range(all_pages)]
    product_list_page = Paginator(product_list, item).page(page_num)
    product_list_json = {"object_list":product_list_page.object_list,
                         "number":product_list_page.number,
                         }#要转换成json,分页后是一个结果集合序列化不了,只能循环赋值

    return resp(json.dumps({"product_list_json":product_list_json,"all_page_list":all_page_list}))