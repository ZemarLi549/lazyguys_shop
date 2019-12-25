"""LazyGuys URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from shop import views
from shop import goods
from shop import login_reg
from shop import user_operations
from shop import product_sort_ajax
from shop import trade
from shop import users
from shop import houtai
from shop import tools
from shop import short_message
from shop import spiders
from django.conf.urls import url, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('vipshipin', views.to_vipshipin),#转到主页页
    path('vipshipin_jiexi', views.vipshipin_jiexi),#转到主页页
    path('', views.to_index),#转到主页页
    path('to_shop_list', views.to_shop_list),#转到商品列表页
    path('to_about_us', views.to_about_us),  # 关于我们!
    path('to_connect_us', views.to_connect_us),  # 联系我们!
    path('page_not_found', views.page_not_found),  # 联系我们!
    path('page_not_host', views.page_not_host),  # 联系我们!
    path('page_error', views.page_error),  # 联系我们!
    path('to_shao_faq',views.to_shao_faq),
    path('to_shop_privacy_policy',views.to_shop_privacy_policy),
    path('to_shop_terms_conditions_page',views.to_shop_terms_conditions_page),
    path('produce_code', login_reg.produce_code),#登录图形验证码
    path('sanfang_init', login_reg.sanfang_init),#登录图形验证码
    path('to_shop_item', views.to_shop_item),#转到单个商品详情页
    path('login_out', views.login_out),#转到单个商品详情页
    path('viewdetails', goods.viewdetails),#处理查看细节按钮,更具ID查询点击商品的所有信息
    path('collect_love', goods.collect_love),#处理用户收藏函数
    path('execute_login', login_reg.execute_login),#判断登录判断!
    path('to_login', login_reg.to_login),#到登录页面!
    path('to_shop_register', login_reg.to_shop_register),#到注册页面!
    path('check_un', login_reg.check_un),#判断登录用户是否正确!
    path('check_reg', login_reg.check_reg),#判断注册用户是否正确!
    path('to_standart', user_operations.to_standart),#到修改信息页面!
    path('to_account', user_operations.to_account),#到个人信息页面!
    path('change_forms', user_operations.change_forms),#到执行修改信息!
    path('qingwen', user_operations.qingwen),#到执行修改信息!
    path('huifu', user_operations.huifu),#到执行修改信息!
    path('richtext_upload', user_operations.richtext_upload),#到执行修改信息!
    path('dianzan', user_operations.dianzan),#到点赞!
    path('uploadfile', user_operations.uploadfile),#到执行修改信息!
    path('ajax_sort', product_sort_ajax.ajax_sort),#到product-list页面后条件筛选函数
    path('to_search_result', product_sort_ajax.to_search_result),#到搜索结果页面后
    path('ajax_sort_search', product_sort_ajax.ajax_sort_search),#到搜索结果页面后进行条件筛选
    path('page_display_search', product_sort_ajax.page_display_search),#到搜索结果页面后进行条件筛选
    path('search_tips', product_sort_ajax.search_tips),#到搜索提示
    path('page_display', product_sort_ajax.page_display),#到搜索提示
    path('to_shop_cart', trade.to_shop_cart),#到购物车页面!
    path('to_checkout', trade.to_checkout),#到结算页面!
    path('checkout_init', trade.checkout_init),#到结算前处理购物车数据页面!
    path('to_myorder', trade.to_myorder),#到我的订单页面
    path('change_paystatus', trade.change_paystatus),#到结算前处理购物车数据页面!
    path('order_execute', trade.order_execute),#处理用户收货地址订单填写自动保存地址信息!
    path('del_order', trade.del_order),#处理用户收货地址订单填写自动保存地址信息!
    path('to_pay_page', trade.to_pay_page),#处理用户收货地址订单填写自动保存地址信息!
    path('alipay_return_url', trade.alipay_return_url),#处理用户收货地址订单填写自动保存地址信息!
    path('alipay_return_notify', trade.alipay_return_notify),#处理用户收货地址订单填写自动保存地址信息!
    path('to_alipay_page', trade.to_alipay_page),#处理用户收货地址订单填写自动保存地址信息!
    path('to_collect', users.to_collect),#到用户收藏页面!
    path('cart_manage', users.cart_manage),#到用户收藏页面!
    path('remove_collect', users.remove_collect),#处理用户取消收藏函数!
    path('to_my_cart', users.to_my_cart),#处理用户取消收藏函数!
    path('del_cart_good', users.del_cart_good),#处理用户取消收藏函数!
    path('to_myshippingaddress', users.to_myshippingaddress),#处理用户取消收藏函数!
    path('del_address', users.del_address),#处理用户取消收藏函数!
    path('add_shippingaddr', users.add_shippingaddr),#处理用户取消收藏函数!
    path('to_admin_index', houtai.to_admin_index),#处理用户取消收藏函数!
    path('loginverify', houtai.loginverify),#处理用户取消收藏函数!
    path('lzxwlglwyh', houtai.to_manage_page),#处理用户取消收藏函数!
    path('to_modify_goods', houtai.to_modify_goods),#处理用户取消收藏函数!
    path('ajax_sort_houtai', houtai.ajax_sort_houtai),#处理用户取消收藏函数!
    path('to_modify_item', houtai.to_modify_item),#处理用户取消收藏函数!
    path('toadministrator', houtai.toadministrator),#处理后台登录磊
    path('modify_good_info', houtai.modify_good_info),#处理用户取消收藏函数!
    path('del_good', houtai.del_good),#处理用户取消收藏函数!
    path('add_good', houtai.add_good),#处理用户取消收藏函数!
    path('del_wenda', houtai.del_wenda),#处理用户取消收藏函数!
    path('del_review', houtai.del_review),#处理用户取消收藏函数!
    path('to_order_center', houtai.to_order_center),#处理用户取消收藏函数!
    path('to_chat', tools.to_chat),#处理用户取消收藏函数!
    path('updateAvatar', tools.updateAvatar),#处理用户取消收藏函数!
    path('update_my_nn', tools.update_my_nn),#处理用户取消收藏函数!
    path('serch_content', tools.serch_content),#处理用户取消收藏函数!
    path('serch_qun_content', tools.serch_qun_content),#处理用户取消收藏函数!
    path('chat_addcontent', tools.chat_addcontent),#处理用户取消收藏函数!
    path('serch_frs', tools.serch_frs),#处理用户取消收藏函数!
    path('rich_send_upload', tools.rich_send_upload),#处理用户取消收藏函数!
    path('search_qun_list', tools.search_qun_list),#处理用户取消收藏函数!
    path('search_user_list', tools.search_user_list),#处理用户取消收藏函数!
    path('add_new_fr', tools.add_new_fr),#处理用户取消收藏函数!
    path('shuaxin_new_fr', tools.shuaxin_new_fr),#处理用户取消收藏函数!
    path('jieshou_new_fr', tools.jieshou_new_fr),#处理用户取消收藏函数!
    path('jujue_new_fr', tools.jujue_new_fr),#处理用户取消收藏函数!
    path('lunxun_header_news', tools.lunxun_header_news),#处理用户取消收藏函数!
    path('shanchutuichu', tools.shanchutuichu),#处理用户取消收藏函数!
    path('create_qun', tools.create_qun),#处理用户取消收藏函数!
    path('yaoqing_fr', tools.yaoqing_fr),#处理用户取消收藏函数!
    path('yaoqing_list', tools.yaoqing_list),#处理用户取消收藏函数!
    path('luxun_news', tools.luxun_news),#处理用户取消收藏函数!
    path('click_remove_news', tools.click_remove_news),#处理用户取消收藏函数!
    path('msg_code_make', short_message.msg_code_make),#处理用户取消收藏函数!
    path('msg_code_verify', short_message.msg_code_verify),#处理用户取消收藏函数!
    path('bd_spider_pic', spiders.bd_spider_pic),#处理用户取消收藏函数!
    path('xuanze_avatar', spiders.xuanze_avatar),#处理用户取消收藏函数!
    path('duibi_jd', spiders.duibi_jd),#处理用户取消收藏函数!
    path('jd_soutu', spiders.jd_soutu),#处理用户取消收藏函数!


    url('', include('social_django.urls', namespace='social'))
]
