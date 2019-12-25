$(function () {
        $('.search-button').click(function () {
            $('.search-box').stop().toggle(500);
           return false;
        });
//两个函数是必须的
    function getcartsession() {
        var cart_goods_ls=[];
        if($.session.get("cart_goods_ls")!=undefined&&$.session.get("cart_goods_ls")!=''){
            cart_goods_ls = JSON.parse( $.session.get("cart_goods_ls") );
        }
        return cart_goods_ls
    }

    function cart_add(cart_goods_ls){
        $('.top-cart-block .scroller').empty();
        $.each(cart_goods_ls,function (index,item) {
            $('.top-cart-block .scroller').append('<li>\n' +
            '                  <a class="goods_id_aaa" href="to_shop_item?goods_id='+item.goods_id+'"><img src="'+item.goods_img+'" alt="Rolex Classic Watch" width="37" height="34"></a>\n' +
            '                  <span class="cart-content-count">x '+item.goods_num+'</span>\n' +
            '                  <strong><a href="to_shop_item?goods_id='+item.goods_id+'">'+item.goods_name+'</a></strong>\n' +
            '                  <span class="cart_color">'+item.goods_color+'</span>\n' +
            '                  <span class="cart_size">'+item.goods_size+'</span>\n' +
            '                  <em class="cart_totalprice">'+item.goods_totalprice+'¥</em>\n' +
            '                  <a href="javascript:void(0);" class="del-goods">&nbsp;</a>\n' +
            '                </li>');
        });
    }
//两个函数是必须的
        cart_add(getcartsession());//初始渲染
        //点击删除购物车缓存商品
        $('.top-cart-block .scroller').on('click','.del-goods',function () {//用bind会出错!
            var cart_goods_ls=getcartsession();
            var $del = $(this);
            var del_goods_index = $del.parent('li').index();
            var cart_goods_ls_del = [];
            var choice_del = confirm('确定删除此类商品?');
            if(choice_del==true){
                var item_num_pre = parseInt($('.top-cart-info-count>span').text());
                $('.top-cart-info-count>span').text(item_num_pre-1);//删除减一项
                $.each(cart_goods_ls,function (index,item) {
                    if(index != del_goods_index){
                        cart_goods_ls_del.push(item);
                    }
                });
                $.session.set("cart_goods_ls",JSON.stringify(cart_goods_ls_del));
                cart_add(cart_goods_ls_del);//渲染更新后的东西

            }

    });
        $('.top-cart-block .btn-clear').click(function () {
            var cart_goods_ls=getcartsession();
            var qingkong = confirm('确定清空购物车?');
            if(qingkong==true){
                cart_goods_ls=[];
                $.session.set("cart_goods_ls",'');
                cart_add(cart_goods_ls);
                $('.top-cart-info-count>span').text(0);
                }

    });
        //退出登录清理缓存
        $('.tuichulogin').click(function () {
            $('.xiaoxi_container').hide();
            var cart_goods_ls=[];
            $.session.set("cart_goods_ls",'');
            cart_add(cart_goods_ls);
            $('.top-cart-info-count>span').text(0);

            $.post('login_out',{},function (data) {
                if(data.status){
                    window.location.href = '/';
                }
            },'json');
        });
        //退出登录清理缓存
        //点击删除购物车缓存商品
        //结算按钮未登录不管用
        $('.top-cart-content-wrapper .btn-primary').click(function () {
            var count = $('.additional-nav>.pull-right>input[type=hidden]').val();
            if (count) {
                if($('.top-cart-block .scroller>li').length>0){
                    $.post('checkout_init',{cart_goods:$.session.get("cart_goods_ls")},function (data) {
                        if(data.status){
                            console.log('能到这跳转');
                            window.location.href = 'to_checkout';
                        }
                    },'json')

                }
                else {
                    alert('购物车为空!');
                }
            }else{
                alert('请先登录再进行结算!');
        }
        });
        //结算按钮未登录不管用
        //查看购物车按钮未登录不管用
        $('.top-cart-content-wrapper .btn-default').click(function () {
            var $viewcart = $(this);
            var count = $('.additional-nav>.pull-right>input[type=hidden]').val();
            if (count) {
                if($('.top-cart-block .scroller>li').length>0){
                    $viewcart.attr('href','to_shop_cart')
                }
                else {
                    alert('购物车为空!');
                }
            }else{
                alert('请先登录再查看购物车!');
        }
        });
        //查看购物车按钮未登录不管用
        //购物车上有几项
        var item_num = $('.top-cart-block .scroller>li').length;
        $('.top-cart-info-count>span').text(item_num);
        //购物车上有几项
        //热搜点击
        $('.resou').click(function () {
            var words = $(this).text();
            $('.search_content').val(words);
        });
        //热搜点击
        //搜索框输入时提示
    $('.search_content').on('input propertychange',function () {
       var search_content = $(this).val();
       $('.serch_kw_list').empty();
       if ($('.search_content').val()!=''){
           $.post('search_tips',{"search_content":search_content},function (data) {
           $.each(data,function (index,item) {
               $('.serch_kw_list').append('<li>'+item.keywords+'</li>')
           })
       },'json')
       }


    });
    //搜索框输入时提示
    $('.serch_kw_list').on('click','li',function () {
        var tip = $(this).text();
        $('.search_content').val(tip);
    });


    //新消息提醒
    if($.session.get("data_last")!=undefined&&$.session.get("data_last")!=''){
        var kkk_last = $.session.get("data_last");
        console.log('qusession:',kkk_last)
        kkk_last = JSON.parse(kkk_last);

        $.each(kkk_last,function (ind,item) {
            $('.xiaoxi_ul').append(item)
        });
        console.log(kkk_last)
    }else {
        console.log('wuwuwuwuwu');
        $('.xiaoxi_ul').append('<img src="/static/MetronicShopUI/assets/register/imgs/loading.gif" alt="loading..." style="width: 24px;height: 24px;">');
    }
    var news_timer=false;
    var news_last;

    var my_username = $('.additional-nav>.pull-right>input[type=hidden]').val();
    if(my_username){
        $('.xiaoxi_container').show();
        lunxun_news();
    }else {
        if (news_timer!=false){
            clearInterval(news_timer);
        }
        $('.xiaoxi_container').hide();
    }
    var lunxun_news_flag = true;
    $('.xiaoxi_img').click(function () {
        lunxun_news_flag = !lunxun_news_flag;
        $('.xiaoxi_ul').toggle(200);
        if(lunxun_news_flag){
            lunxun_news()
        }else {
            clearInterval(news_timer);
        }
    });


    function lunxun_news() {

        var my_username = $('.additional-nav>.pull-right>input[type=hidden]').val();
        if (my_username){
            news_timer = setInterval(function () {
            var data_last = [];
            if($.session.get("news_last")!=undefined&&$.session.get("news_last")!=''){
                news_last = $.session.get("news_last");
            }
            $.post('lunxun_header_news',{news_last:news_last,my_username:my_username},function (data) {
                if(data.status){
                    $('.xiaoxi_ul').empty();
                    $.each(data.new_frs,function (index,fr) {
                        $('.xiaoxi_ul').prepend('<li><a href="to_chat"><strong>'+fr.nickname+'</strong>接受你的好友请求了,可以去撩啦!</a></li>')
                        data_last.push('<li><a href="to_chat"><strong>'+fr.nickname+'</strong>接受你的好友请求了,可以去撩啦!</a></li>')
                    });
                    $.session.set("data_last",JSON.stringify(data_last));
                }else {
                    if(data.status_news){
                        var news_compare = data.news_compare;
                        $('.xiaoxi_ul').empty();
                        var kkk = 0;
                        $.each(news_compare,function (key,val) {
                            if(val[0]>0){
                                kkk++;
                                $('.xiaoxi_ul').append('<li><a href="to_chat"><strong>'+val[1]+'</strong>给你发来<em>'+val[0]+'</em>条新消息</a></li>')
                                data_last.push('<li><a href="to_chat"><strong>'+val[1]+'</strong>给你发来<em>'+val[0]+'</em>条新消息</a></li>')
                                $.session.set("data_last",JSON.stringify(data_last));
                            }
                        });
                        if(kkk==0){
                            $('.xiaoxi_ul').append('<p>暂无最新消息</p>');
                            data_last.push('<p>暂无最新消息</p>');
                            console.log('zhelishi:',data_last);
                            console.log('zhejj:',JSON.stringify(data_last));
                            $.session.set("data_last",JSON.stringify(data_last));
                        }
                    }else {
                        $('.xiaoxi_ul').empty();
                        $('.xiaoxi_ul').append('<p>暂无最新消息</p>');
                        data_last.push('<p>暂无最新消息</p>');
                        $.session.set("data_last",JSON.stringify(data_last));
                        $.session.set('news_last',JSON.stringify(data.news_init))
                    }
                }
            },'json');

        },10000)
        }

    };


    //新消息提醒
});