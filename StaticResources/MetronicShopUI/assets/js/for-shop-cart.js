$(function () {
    //获取购物车缓存商品列表
    var cart_goods=[];
    if($.session.get("cart_goods_ls")!=undefined&&$.session.get("cart_goods_ls")!=''){
        cart_goods = JSON.parse( $.session.get("cart_goods_ls") );
    }
    //获取购物车缓存商品列表
    //选中取消
    $('.goods-page').on('click','.xuanzhong',function () {
        $(this).parent().parent().addClass('cartbianhui');
        $(this).stop().hide(200).siblings().show(200);
        var danxiangzongjia=$(this).parents('.goods-page-ref-no').siblings('.goods-page-total').children('strong').children('span').text();
            var danzong=Number(danxiangzongjia);
            var zongjia=$(".shopping-total-price>.price>span").text();
            var zongjianumber=Number(zongjia);
            zongjianumber=zongjianumber-danzong;
            // zongjianumber = Math.round(zongjianumber*100)/100;
            zongjianumber = zongjianumber.toFixed(2);
            $(".shopping-total-price>.price>span").text(zongjianumber)
    });
    $('.goods-page').on('click','.quxiao',function () {
        $(this).parent().parent().removeClass('cartbianhui');
        $(this).stop().hide(200).siblings().show(200);
        var danxiangzongjia=$(this).parents('.goods-page-ref-no').siblings('.goods-page-total').children('strong').children('span').text();
            var danzong=Number(danxiangzongjia);
            var zongjia=$(".shopping-total-price>.price>span").text();
            var zongjianumber=Number(zongjia);
            zongjianumber=zongjianumber+danzong;
            // zongjianumber = Math.round(zongjianumber*100)/100;
            zongjianumber = zongjianumber.toFixed(2);
            $(".shopping-total-price>.price>span").text(zongjianumber)
    });
    //选中取消
    //渲染到页面上一行一行显示
    var totalpriceinit = 0;
    $.each(cart_goods,function (index,item) {
        $('.table-wrapper-responsive>table>tbody').append('<tr>\n' +
            '                    <input type="hidden" value="'+item.goods_id+'">\n'+
            '                    <td class="goods-page-image">\n' +
            '                      <a href="to_shop_item?good_id='+item.goods_id+'"><img src="'+item.goods_img+'" alt="Berry Lace Dress"></a>\n' +
            '                    </td>\n' +
            '                    <td class="goods-page-description">\n' +
            '                      <h3><a href="to_shop_item?good_id='+item.goods_id+'">'+item.goods_name+'</a></h3>\n' +
            '                      <p><strong>库存:<span>'+item.goods_stock+'</span></strong> -- 颜色: <span>'+item.goods_color+'</span></p>\n' +
            '                      <em>尺寸种类: <span>'+item.goods_size+'</span></em>\n' +
            '                    </td>\n' +
            '                    <td class="goods-page-ref-no">\n' +
            '                        <img src="/static/MetronicShopUI/assets/register/imgs/right.png" class="xuanzhong" alt="">\n' +
            '                        <img src="/static/MetronicShopUI/assets/register/imgs/cha.png" class="quxiao" alt="">\n' +
            '                    </td>\n' +
            '                    <td class="goods-page-quantity">\n' +
            '                      <div class="product-quantity">\n' +
            '                          <input id="product-quantity2" type="text" value="'+item.goods_num+'" readonly class="form-control input-sm">\n' +
            '                      </div>\n' +
            '                    </td>\n' +
            '                    <td class="goods-page-price">\n' +
            '                      <strong><span>'+item.goods_unitprice+'</span>¥</strong>\n' +
            '                    </td>\n' +
            '                    <td class="goods-page-total">\n' +
            '                      <strong><span>'+item.goods_totalprice+'</span>¥</strong>\n' +
            '                    </td>\n' +
            '                    <td class="del-goods-col">\n' +
            '                      <a class="del-goods" href="javascript:;">&nbsp;</a>\n' +
            '                    </td>\n' +
            '                  </tr>');
        totalpriceinit = (Number(totalpriceinit)+Number(item.goods_totalprice)).toFixed(2);
        // totalpriceinit = Math.round(totalpriceinit*100)/100;
    });
    $('.shopping-total>ul>.shopping-total-price>.price>span').text(totalpriceinit);//初始总价渲染
    //渲染到页面上一行一行显示
    //高龙写改数量,删除,总价修改
    $('.goods-page').on('click','.quantity-up',function () {
        var $up = $(this);
        var shuliang = Number($up.parents('.goods-page-quantity').find('#product-quantity2').val());
        var stock = Number($up.parents('.goods-page-quantity').siblings('.goods-page-description').find('p>strong>span').text());

        if(shuliang<stock){
            var danjia = $up.parents('.goods-page-quantity').siblings('.goods-page-price').find('span').text();
            var danhangzongjia = $up.parents('.goods-page-quantity').siblings('.goods-page-total').find('span').text();
            danhangzongjia = (Number(danhangzongjia)+Number(danjia)).toFixed(2);
            // danhangzongjia = Math.round(danhangzongjia*100)/100;
            $up.parents('.goods-page-quantity').siblings('.goods-page-total').find('span').text(danhangzongjia);
            genggaizongjia()
        }else {
            $up.parents('.goods-page-quantity').find('#product-quantity2').val(stock);
            alert('库存不足了啊兄弟!')
        }

    });
    $('.goods-page').on('click','.quantity-down',function () {
        var $dowm = $(this);
        var shuliang = Number($dowm.parents('.goods-page-quantity').find('#product-quantity2').val());
        console.log('这里才是',shuliang);
        if(shuliang>0){
            var danjia = $dowm.parents('.goods-page-quantity').siblings('.goods-page-price').find('span').text();
            var danhangzongjia = $dowm.parents('.goods-page-quantity').siblings('.goods-page-total').find('span').text();
            danhangzongjia = (Number(danhangzongjia)-Number(danjia)).toFixed(2);
            // danhangzongjia = Math.round(danhangzongjia*100)/100;
            $dowm.parents('.goods-page-quantity').siblings('.goods-page-total').find('span').text(danhangzongjia);
            genggaizongjia()
        }else {
            $dowm.parents('.goods-page-quantity').find('#product-quantity2').val('1');
            alert('再减我就要倒贴了啊兄弟!')
        }

    });
    //高龙写改数量,删除,总价修
    function genggaizongjia() {
       var len= $(".goods-page-total").length;
       var zongjia=0;
        for (let i = 0; i <len ; i++) {
            if (i!=0){
                var text=$(".goods-page-total").eq(i).children('strong').children('span').text();
                var numeber=Number(text);
                zongjia=Number(zongjia)+numeber;
                zongjia = zongjia.toFixed(2);
                // zongjia = Math.round(zongjia*100)/100;
             }
        }
        $(".shopping-total-price>.price>span").text(zongjia);
    }

        $(".goods-page").on('click','.del-goods',function () {
            var yaoshanchudanxiangzongjia=$(this).parents(".del-goods-col").siblings(".goods-page-total").children('strong').children('span').text();
            var danzong=Number(yaoshanchudanxiangzongjia);
            var shanchuhouzongjia=$(".shopping-total-price>.price>span").text();
            var number1=Number(shanchuhouzongjia);
            number1=number1-danzong;
            // number1 = Math.round(number1*100)/100;
            number1 = number1.toFixed(2);
            $(".shopping-total-price>.price>span").text(number1);
            $(this).parents(".del-goods-col").parents("tr").remove();
        });

    //高龙写改数量,删除,总价修改
    //到结算页面判断
    $('.goods-page .btn-primary').click(function () {
        var total_flag = $('.shopping-total>ul>.shopping-total-price>.price>span').text();
        if (total_flag!='0'){//如果总价为空的话不能到结算页面!
            //ajax传递数据
            var cart_goods_modify=[];
            var len_tr = $('.table-wrapper-responsive>table>tbody>tr').length;
            console.log('共几行',len_tr);
            for(var i=0;i<len_tr;i++){
                var $tr = $('.table-wrapper-responsive>table>tbody>tr').eq(i);
                if($tr.hasClass('cartbianhui')){
                    console.log('第',i,'行没选中')
                }else {
                    console.log('第',i,'选中了');
                    var goods_id = $tr.find('input[type=hidden]').val();
                    var goods_img = $tr.find('.goods-page-image>a>img').attr('src');
                    var goods_stock = $tr.find('.goods-page-description>p>strong>span').text();
                    var goods_num = $tr.find('#product-quantity2').val();
                    var goods_name = $tr.find('.goods-page-description>h3>a').text();
                    var good_size = $tr.find('.goods-page-description>em>span').text();
                    var goods_color = $tr.find('.goods-page-description>p>span').text();
                    var goods_unitprice = $tr.find('.goods-page-price>strong>span').text();
                    var goods_totalprice = $tr.find('.goods-page-total>strong>span').text();
                    var good_info = {goods_id:goods_id,goods_img:goods_img,goods_num:goods_num,goods_name:goods_name,good_size:good_size,goods_color:goods_color,goods_unitprice:goods_unitprice,goods_totalprice:goods_totalprice,goods_stock:goods_stock};
                    cart_goods_modify.push(good_info);
                }

            }

            $.post('checkout_init',{cart_goods:JSON.stringify(cart_goods_modify)},function (data) {
                if(data.status){
                    window.location.href = 'to_checkout';
                }else {
                    alert(data.tips)
                }
            },'json');
            //ajax传递数据

        }else {
            alert('请添加或勾选商品再结算!')
        }
    }
    )
    //到结算页面判断
});