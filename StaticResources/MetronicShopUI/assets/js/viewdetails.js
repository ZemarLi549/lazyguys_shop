$(function () {
    //fancybox-fast-view查看细节按钮click后内部样式改变
    function panduan(flag){//处理登录用户是否收藏该商品函数
        if(flag==true){
                      $('#img_collect').attr({'src':'/static/MetronicShopUI/assets/register/imgs/collectred.png','title':"取消收藏该商品"});
                  }else {
                      $('#img_collect').attr({'src':'/static/MetronicShopUI/assets/register/imgs/collectyellow.png','title':'点击收藏该商品'});
                  }
    }
    var collect_status = false;//判断登录用户是否收藏该商品初始化
    $('body').on('click','.fancybox-fast-view',function () {

        $('#product-pop-up #product-quantity').val('1');//初始化数量值为1;
        var goods_id = $(this).parents('.product-item').find('.hide_id').val();
        var username = $('.additional-nav>.pull-right>input[type=hidden]').val();
        $('#product-pop-up>.hide_id').val(goods_id);
        $('#product-pop-up .btn-default').attr('href','to_shop_item?goods_id='+goods_id+'');
        $.post('viewdetails',{goods_id:goods_id,username:username},function (datas) {
            var data = datas.json_goods_info;
            if(datas.fav_flag=='YES'){//判断登录用户是否收藏该商品,收藏使爱心变红
                // console.log('yesyes');
                collect_status=true;
            }else {
                collect_status = false;//判断登录用户是否收藏该商品初始化
            }
            panduan(collect_status);//打开view页面先判断一下是否收藏
            // console.log(data);
            $('#product-pop-up .product-main-image img').attr('src',data[0].fields.goods_img[0]);
            $('#product-pop-up .product-other-images>a:eq(0)>img').attr('src',data[0].fields.goods_img[0]);
            $('#product-pop-up .product-other-images>a:eq(1)>img').attr('src',data[0].fields.goods_img[1]);
            $('#product-pop-up .product-other-images>a:eq(2)>img').attr('src',data[0].fields.goods_img[2]);
            $('#product-pop-up .col-xs-9>h1').text(data[0].fields.goods_brief);
            $('#product-pop-up .col-xs-9>h5').text(data[0].fields.name);
            $('#product-pop-up .price>strong>span').text(data[0].fields.current_price);
            $('#product-pop-up .price>em>span').text(data[0].fields.original_price);
            $('#product-pop-up .availability>strong').text(data[0].fields.goods_stock);
            $('#product-pop-up .description>p').text(data[0].fields.goods_desc);
            $('#product-pop-up .liulanliang').text(data[0].fields.views_count);
            $('#product-pop-up .shoucangliang').text(data[0].fields.fav_num);
            $('#product-pop-up .haopingliang').text(data[0].fields.haoping);
            $('#product-pop-up .xiaoshouliang').text(data[0].fields.sale_count);


            //给上尺寸种类和颜色
            var size_type_list = datas.size_type_list;
            var color_list = datas.color_list;
            $('#product-pop-up .product-page-options>.pull-left:eq(0)>select').empty();//先清空上一次浏览的
            $.each(size_type_list,function (index,item) {
                if (item!=''){
                    $('#product-pop-up .product-page-options>.pull-left:eq(0)>select').append('<option>'+item+'</option>');
                }
            });
            $('#product-pop-up .product-page-options>.pull-left:eq(1)>select').empty();//先清空上一次浏览的
            $.each(color_list,function (index,item) {
                if (item!=''){
                    $('#product-pop-up .product-page-options>.pull-left:eq(1)>select').append('<option>'+item+'</option>');
                }
            });

            if(data[0].fields.is_sale){
                $('.product-main-image').append('<div class="sticker sticker-sale"></div>')
            }
            if(data[0].fields.is_new){
                $('.product-main-image').append('<div class="sticker sticker-new"></div>')
            }
        },'json')
    });
    //fancybox-fast-view查看细节按钮click后内部样式改变
    //放大镜

    $('.light-zoom').lightzoom({
		            zoomPower   : 2,    //Default
		            glassSize   : 180,  //Default
		        });
    //放大镜
    //点击附图切换
    $('.product-other-images>a').click(function () {
        $(this).addClass('active').siblings().removeClass('active');
        var imgsrc = $(this).find('img').attr('src');
        $('.product-main-image>img').attr('src',imgsrc)
    });
    //点击附图切换
    //添加购物车使用$.session方法
    //两个函数是必须的
    function getcartsession() {
        var cart_goods_ls=[];
        if($.session.get("cart_goods_ls")!=undefined&&$.session.get("cart_goods_ls")!=''){
            console.log('session有值啊');
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


 //点击添加购物车
    $('#product-pop-up .btn-primary').click(function () {
        //未登录不能添加购物车
        var count = $('.additional-nav>.pull-right>input[type=hidden]').val();
        if (count) {
            var cart_goods_ls=getcartsession();
            var goods_stock = $('#product-pop-up .availability>strong').text();
            var goods_id = $('#product-pop-up>.hide_id').val();
            var goods_img = $('#product-pop-up .product-main-image>img').attr('src');
            var goods_num = $('#product-pop-up #product-quantity').val();
            var goods_name = $('#product-pop-up h5').text();
            var goods_size = $('#product-pop-up .product-page-options>.pull-left:eq(0)>select').val();
            var goods_color = $('#product-pop-up .product-page-options>.pull-left:eq(1)>select').val();
            var goods_unitprice = $('#product-pop-up .price>strong>span').text();
            var goods_totalprice = (Number(goods_unitprice)*Number(goods_num)).toFixed(2);
            var good_info = {goods_id:goods_id,goods_img:goods_img,goods_num:goods_num,goods_name:goods_name,goods_size:goods_size,goods_color:goods_color,goods_unitprice:goods_unitprice,goods_totalprice:goods_totalprice,goods_stock:goods_stock};
            cart_goods_ls.push(good_info);
            console.log(cart_goods_ls);
            var cart_goods_ls_str = JSON.stringify(cart_goods_ls);
            $.session.set("cart_goods_ls",cart_goods_ls_str);//缓存购物车内容
            $.post('cart_manage',{good_info:JSON.stringify(good_info)},function (data) {
                if(data.status){
                    console.log('存购物车库了')
                }
            },'json');
            cart_goods_ls = JSON.parse( $.session.get("cart_goods_ls") );
            cart_add(cart_goods_ls);//重新渲染购物车
            var item_num_pre = parseInt($('.top-cart-info-count>span').text());
            $('.top-cart-info-count>span').text(item_num_pre+1);//增加后项目加一
            alert("添加购物车成功,可去购物车查看^_^");
        }else{
            alert('请先登录再进行添加购物车!');
        }
        //未登录不能添加购物车


    });
    //添加购物车
    //购买量大于库存报错
    $('#product-pop-up').on('click','.quantity-up',function () {
        var $up = $(this);
        var shuliang = Number($up.parents('.product-quantity').find('#product-quantity').val());
        var stock = Number($up.parents('.product-page-cart').siblings('.price-availability-block').find('.availability>strong').text());
        console.log('这里才是',shuliang,stock);
        if(shuliang<stock){

        }else {
            $up.parents('.product-quantity').find('#product-quantity').val(stock);
            alert('库存量不足啊兄弟!')
        }

    });
    $('#product-pop-up').on('click','.quantity-down',function () {
        var $down = $(this);
        var shuliang = Number($down.parents('.product-quantity').find('#product-quantity').val());
        if(shuliang>0){

        }else {
            $down.parents('.product-quantity').find('#product-quantity').val('1');
            alert('不能再减了啊兄弟!')
        }

    });
    //购买量大于库存报错
    // 收藏爱心点击收藏或取消
    $('#img_collect').click(function () {
        var count = $('.additional-nav>.pull-right>input[type=hidden]').val();
        var goods_id = $('#product-pop-up').children('.hide_id').val();
        if (count) {
            collect_status = !collect_status;
            $.post('collect_love',{un:count,goods_id:goods_id,collect_status:collect_status},function (data) {
                panduan(collect_status);
                $('.shoucangliang').text(data.fav_num);
            },'json');
            }else{
                alert('请先登录再进行收藏!');
        }
    })
    // 收藏爱心量点击收藏或取消
});