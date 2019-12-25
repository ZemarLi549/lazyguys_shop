from django.shortcuts import render,HttpResponse as resp
from . import models
import json
import random
import math
from django.core import serializers
from django.db.models import Q
# render显示各个页面模块.
def to_json(class_list):
    json_list = serializers.serialize("json", class_list)
    json_list = json.loads(json_list)
    if json_list:
        for item in json_list:
            item['fields']['goods_img'] = json.loads(item['fields']['goods_img'])
            item['fields']['parameter'] = json.loads(item['fields']['parameter'])
    return  json_list
def login_out(request):
    if 'user_info' in request.session.keys():
        request.session.pop('user_info')
    return resp(json.dumps({"status":True}))




def to_index(request):

    """
    主页面shop-index
    """
    if 'user_info' in request.session.keys():
        username = request.session['user_info']['username']
        user_info = models.User.objects.filter(username=username)[0]
        frs_quns = json.loads(user_info.frs_quns)
        frs_list = frs_quns['frs']
        request.session['frs_list'] = frs_list
    #初始用户

    json_new_list=json_fav_list=json_hao_list=[]
    #大轮播图列表
    lunbo_list = models.Goods.objects.all()[:7]
    lunbo_list = to_json(lunbo_list)
    # 大轮播图列表


    # 三栏显示收藏量排序
    fav_list = models.Goods.objects.order_by('-fav_num')[:9]
    json_fav_list = to_json(fav_list)
    #三栏显示


    #两栏显示
    hao_list = models.Goods.objects.order_by('-haoping')[:6]
    json_hao_list = to_json(hao_list)
    #两栏显示


    #首页新品前12条随机
    new_len = models.Goods.objects.filter(is_new=True).count()
    if new_len<=13:
        lennew = new_len
    else:
        lennew = new_len-13
    jj = random.randint(0,lennew)
    new_list = models.Goods.objects.filter(is_new=True)[jj:jj+12]
    json_new_list = to_json(new_list)
    #首页新品前12条随机

    # 按照浏览最多对商品渲染
    views_count_list = models.Goods.objects.order_by('-views_count')[:4]
    views_count_list = to_json(views_count_list)
    # print('浏览量',views_count_list)
    # 按照浏览最多对商品渲染

    # 按照热销对商品渲染
    sale_count_list = models.Goods.objects.order_by('-sale_count')[:4]
    sale_count_list = to_json(sale_count_list)
    # print('销售量',sale_count_list)
    # 按照热销对商品渲染
    # 返回热搜词列表
    hotwords_list = models.HotSearchWords.objects.all().order_by('-index')[:6]
    request.session['hotwords_list'] = json.loads( serializers.serialize('json',hotwords_list) )
    # 返回热搜词列表
    request.session['sale_new_top4']={"sale_count_list": sale_count_list, "views_count_list": views_count_list,}
    return render(request,'shop-index.html',{"new_list":json_new_list,"fav_list":json_fav_list,"hao_list":json_hao_list,"lunbo_list":json.dumps(lunbo_list)})
def to_shop_list(request):
    '''
    商品列表页面shop-product-list
    '''
    # 返回热搜词列表
    hotwords_list = models.HotSearchWords.objects.all().order_by('-index')[:6]
    request.session['hotwords_list'] = json.loads(serializers.serialize('json', hotwords_list))
    # 返回热搜词列表
    # 第一种渲染商品列表:通过header或者左端列表跳转的情况下(一级分类不可能为空值)
    c1 = request.GET.get('c1')
    c2 = request.GET.get('c2')
    c3 = request.GET.get('c3')
    c4 = request.GET.get('c4')
    product_list = models.Goods.objects.all()
    #判断分类一级
    if c1 == '男士专区':
        cc1 = "men"
    elif c1 == '女士专区':
        cc1 = "women"
    elif c1 == '儿童专区':
        cc1 = "children"
    else:
        cc1 = ""
    # 判断分类二级
    if c2 == "鞋子":
        cc2 = "shoes"
    elif c2 == "服装":
        cc2 = "clothes"
    elif c2 == "饰品":
        cc2 = "decorations"
    else:
        cc2 = ""
    #判断三级类目
    if c3 == "运动鞋":
        cc3 = "yundong"
    elif c3 == "可爱风":
        cc3 = "keai"
    elif c3 == "休闲鞋":
        cc3 = "xiuxian"
    elif c3 == "酷炫风":
        cc3 = "kuxuan"
    elif c3 == "休闲风":
        cc3 = "xiuxian"
    elif c3 == "冬季潮品":
        cc3 = "dongji"
    elif c3 == "夏季精品":
        cc3 = "xiaji"
    elif c3 == "春秋热卖":
        cc3 = "chunqiu"
    elif c3 == "潮流风":
        cc3 = "chaoliu"
    elif c3 == "口罩":
        cc3 = "kouzhao"
    elif c3 == "帽子":
        cc3 = "maozi"
    elif c3 == "手套":
        cc3 = "shoutao"
    elif c3 == "袜子":
        cc3 = "wazi"
    elif c3 == "篮球鞋":
        cc3 = "lanqiu"
    elif c3 == "皮鞋":
        cc3 = "pixie"
    elif c3 == "商务风":
        cc3 = "shangwu"
    elif c3 == "运动风":
        cc3 = "yundong"
    elif c3 == "腰带":
        cc3 = "yaodai"
    elif c3 == "领带":
        cc3 = "lingdai"
    elif c3 == "靴子":
        cc3 = "xuezi"
    elif c3 == "高跟鞋":
        cc3 = "gaogeng"
    else:
        cc3 = ""
    #四级分类
    if c4 == "阿迪达斯":
        cc4 = "adidas"
    elif c4 == "耐克":
        cc4 = "nike"
    elif c4 == "安踏":
        cc4 = "anta"
    elif c4 == "花花公子":
        cc4 = "playboy"
    elif c4 == "冠军":
        cc4 = "champion"
    elif c4 == "彪马":
        cc4 = "puma"
    elif c4 == "飒拉":
        cc4 = "zara"
    elif c4 == "其它品牌":
        cc4 = "others"
    else:
        cc4 = ""
    category = {"c1": c1, "c2": c2, "c3": c3, "c4": c4}
    # print(cc1, cc2, cc3, cc4)

    if cc1:
        product_list = models.Goods.objects.filter(category_yi=cc1)
        if cc4:#通过专区下的品牌图标直接进入
            product_list = models.Goods.objects.filter(category_yi=cc1,category_si=cc4)
            pass
        if cc2:
            product_list = models.Goods.objects.filter(category_yi=cc1,category_er=cc2)
            if cc3:
                product_list = models.Goods.objects.filter(category_yi=cc1, category_er=cc2,category_san=cc3)
                pass
            pass
    elif cc1=='' and cc2=='' and cc3 == '' and cc4 != '':#通过分类列表中的品牌专区进入
        product_list = models.Goods.objects.filter(category_si=cc4)
        # print('通过分类跳转商品列表页!')

    # 第一种渲染商品列表:通过header跳转的情况下


    # 是否新品热卖商品渲染
    msg = request.GET.get('msg','NO')
    if msg=='新品服装':
        product_list = models.Goods.objects.filter(category_er='clothes',is_new=True)
    elif msg=='新品鞋':
        product_list = models.Goods.objects.filter(category_er='shoes', is_new=True)
    elif msg=='新品饰品':
        product_list = models.Goods.objects.filter(category_er='decorations', is_new=True)
    elif msg=='热卖服装':
        product_list = models.Goods.objects.filter(category_er='clothes', is_sale=True)
    elif msg=='热卖鞋':
        product_list = models.Goods.objects.filter(category_er='decorations', is_sale=True)
    elif msg=='热卖饰品':
        product_list = models.Goods.objects.filter(category_er='shoes', is_sale=True)
    else:
        print('没有通过选择新品或热卖进入商品列表页!')
    # 是否新品热卖商品渲染

    # 按照浏览最多对商品渲染

    views_count = request.GET.get('views_count','NO')
    if views_count=='浏览最多':
        product_list = models.Goods.objects.order_by('-views_count')
        print('通过选择浏览最多进入商品列表页!')
    # 按照浏览最多对商品渲染

    # 按照热销对商品渲染

    sale_count = request.GET.get('sale_count', 'NO')
    if sale_count == '本店热销':
        product_list = models.Goods.objects.order_by('-sale_count')
        print('通过选择本店热销进入商品列表页!')
    # 按照热销对商品渲染

    product_list = to_json(product_list)
    request.session['product_list'] = {"product_list": product_list}
    request.session['product_list_page'] = {"product_list": product_list}#缓存分类后用分页
    #畅销前四商品本页面并且是sale或者new的
    # print('到list页面', product_list)
    relative_sale_list = []#为你推荐
    for item in product_list:
        if item['fields']['is_sale'] == True or item['fields']['is_new'] == True:
            relative_sale_list.append(item)
    relative_sale_list.sort(key=lambda item: (int(item['fields']['sale_count'])),reverse=True)
    relative_sale_list = relative_sale_list[:10]
    random.shuffle(relative_sale_list)
    relative_sale_list = relative_sale_list[:4]#随机展示前10的4哥产品
    #畅销前四商品本页面
    #分页
    count = len(product_list)
    item = 9
    all_pages = math.ceil(count/item)
    all_page_list = [i+1 for i in range(all_pages)]
    product_list_page = product_list[:9]
    #分页
    return render(request, 'shop-product-list.html', {"category": category,"new_sale":msg,"sale_count":sale_count,"views_count":views_count,"product_list": product_list_page,"all_page_list":all_page_list,"relative_sale_list":relative_sale_list})
def to_shop_item(request):
    '''
    单个商品详情页面shop-item
    '''
    # 返回热搜词列表
    hotwords_list = models.HotSearchWords.objects.all().order_by('-index')[:6]
    request.session['hotwords_list'] = json.loads(serializers.serialize('json', hotwords_list))
    # 返回热搜词列表
    # 如果用户缓存不存在就加上这几句
    if 'user_info' in request.session.keys():
        user = request.session['user_info']
        username = user['username']
    else:
        username = ''
    # 如果用户缓存不存在就加上这几句
    goods_id = request.GET.get('goods_id')
    # print(goods_id)
    if username:
        flag_collect = models.UserFav.objects.filter(username=username, goods_id=goods_id).count()
        if flag_collect:
            # print('到yes')
            fav_flag = "YES"
        else:
            # print('到no')
            fav_flag = "NO"
    else:
        # print('到no')
        fav_flag = "NO"    #判断初始是否收藏


    goods_info = models.Goods.objects.filter(id=goods_id)
    if goods_info:
        # 按照参数栏给尺寸种类分
        parameter = goods_info[0].parameter
        size_type = json.loads(parameter)[2].strip('"')
        size_type_list = size_type.split('款')
        color = json.loads(parameter)[3].strip('"')
        color_list = color.split('色')
        # 按照参数栏给尺寸种类分
        #推荐相关商品
        category_yi = goods_info[0].category_yi
        category_er = goods_info[0].category_er
        relative_list = models.Goods.objects.filter(Q(category_yi=category_yi)&
                                                    Q(category_er=category_er)&
                                                    ~Q(id=goods_id)).order_by('-views_count')[:4]
        relative_list = to_json(relative_list)
        #推荐相关商品
        #浏览量加一
        views_count_new = goods_info[0].views_count + 1
        models.Goods.objects.filter(id=goods_id).update(views_count=views_count_new)
        # 浏览量加一
        json_goods_info = to_json(goods_info)
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
        return render(request, 'shop-item.html',
                      {"goods_info": json_goods_info[0], "fav_flag": fav_flag, "relative_list": relative_list,
                       "reviews_list": reviews_list, "size_type_list": size_type_list, "color_list": color_list,
                       "wenda_list": wenda_list})
    else:#被删除了这个商品
        return resp('此商品已被可恶的管理员删除了!啊啊啊')




#关于我们:
def to_about_us(request):
    return render(request,'about_us.html')

#联系我们:
def to_connect_us(request):
    return render(request,'connect_us.html')



#404,403,500页面:
def page_not_found(request):
    return render(request,'404.html')
def page_not_host(request):
    return render(request,'403.html')
def page_error(request):
    return render(request,'500.html')
#隐私政策啥的
def to_shao_faq(request):
    return render(request,'shop-faq.html')

def to_shop_privacy_policy(request):
    return render(request,'shop-privacy-policy.html')

def to_shop_terms_conditions_page(request):
    return render(request,'shop-terms-conditions-page.html')
#隐私政策啥的
# from django.views.decorators.csrf import csrf_protect
# @csrf_protect
def to_vipshipin(request):
    return render(request,'vipshipin.html')
def vipshipin_jiexi(request):
    wangzhi = request.GET.get('wangzhi')
    print(wangzhi)
    if wangzhi:
        return render(request,'vipshipinjiexi.html',{'wangzhi':wangzhi})
    else:
        return resp('<h1>请输入正确的网址！</h1>')


