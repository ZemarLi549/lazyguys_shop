$(function () {
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
            '                  <span class="cart_size">'+item.good_size+'</span>\n' +
            '                  <em class="cart_totalprice">'+item.goods_totalprice+'¥</em>\n' +
            '                  <a href="javascript:void(0);" class="del-goods">&nbsp;</a>\n' +
            '                </li>');
        });
    }
//两个函数是必须的


 //点击添加购物车
    $('.goods-page').on('click','.add-goods',function () {
        var cart_goods_ls=getcartsession();
        var goods_stock = $('#product-pop-up .availability>strong').text();
        var goods_id = $('#product-pop-up>.hide_id').val();
        var goods_img = $('#product-pop-up .product-main-image>img').attr('src');
        var goods_num = $('#product-pop-up #product-quantity').val();
        var goods_name = $('#product-pop-up h5').text();
        var good_size = $('#product-pop-up .product-page-options>.pull-left:eq(0)>select').val();
        var goods_color = $('#product-pop-up .product-page-options>.pull-left:eq(1)>select').val();
        var goods_unitprice = $('#product-pop-up .price>strong>span').text();
        var goods_totalprice = Number(goods_unitprice)*Number(goods_num);
        var good_info = {goods_id:goods_id,goods_img:goods_img,goods_num:goods_num,goods_name:goods_name,good_size:good_size,goods_color:goods_color,goods_unitprice:goods_unitprice,goods_totalprice:goods_totalprice,goods_stock:goods_stock};
        cart_goods_ls.push(good_info);
        console.log(cart_goods_ls);
        var cart_goods_ls_str = JSON.stringify(cart_goods_ls);
        $.session.set("cart_goods_ls",cart_goods_ls_str);
        cart_goods_ls = JSON.parse( $.session.get("cart_goods_ls") );
        cart_add(cart_goods_ls);
        alert("添加购物车成功,可去购物车查看^_^");

    });
    //添加购物车
    //移出收藏商品
    $('.del-goods-col>a').click(function () {
        var $del = $(this);

        var con = confirm('确认移出收藏吗?');
        if (con){
            var goods_id = $del.parent().parent().find('input[type=hidden]').val();
            $.post('remove_collect',{get_goods_id:goods_id},function (data) {
                if(data.status){
                    window.location.href = 'to_collect';
                }
                },'json')
        }
        //移出收藏商品
    })
});