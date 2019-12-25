$(function () {
    //放大镜
    $('.light-zoom').lightzoom({
		            zoomPower   : 2,    //Default
		            glassSize   : 180,  //Default
		        });
    //放大镜
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
    $('.duibi').click(function () {
        var goods_name = $('.product-page h1').text();
        $.get('duibi_jd',{goods_name:goods_name},function (data) {
            if(data.status){
                window.location.href = 'jd_soutu';
            }
        },'json')
    });
    $('.product-page-cart>.btn-primary').click(function () {
        var count = $('.additional-nav>.pull-right>input[type=hidden]').val();
        if (count) {
            var cart_goods_ls = getcartsession();
            var goods_stock = $('.product-page .availability>strong').text();
            var goods_id = $('.product-page>.hide_id').val();
            var goods_img = $('.product-page .product-main-image>img').attr('src');
            var goods_num = $('.product-page #product-quantity').val();
            var goods_name = $('.product-page h1').text();
            var goods_size = $('.product-page .product-page-options>.pull-left:eq(0)>select').val();
            var goods_color = $('.product-page .product-page-options>.pull-left:eq(1)>select').val();
            var goods_unitprice = $('.product-page .price>strong>span').text();
            var goods_totalprice = (Number(goods_unitprice) * Number(goods_num)).toFixed(2);
            var good_info = {
                goods_id: goods_id,
                goods_img: goods_img,
                goods_num: goods_num,
                goods_name: goods_name,
                goods_size: goods_size,
                goods_color: goods_color,
                goods_unitprice: goods_unitprice,
                goods_totalprice: goods_totalprice,
                goods_stock: goods_stock
            };
            cart_goods_ls.push(good_info);
            console.log(cart_goods_ls);
            var cart_goods_ls_str = JSON.stringify(cart_goods_ls);
            $.session.set("cart_goods_ls", cart_goods_ls_str);//缓存购物车内容
            $.post('cart_manage', {good_info: JSON.stringify(good_info)}, function (data) {
                if (data.status) {
                    console.log('存购物车库了')
                }
            }, 'json');
            cart_goods_ls = JSON.parse($.session.get("cart_goods_ls"));
            cart_add(cart_goods_ls);//重新渲染购物车
            var item_num_pre = parseInt($('.top-cart-info-count>span').text());
            $('.top-cart-info-count>span').text(item_num_pre + 1);//增加后项目加一
            alert("添加购物车成功,可去购物车查看^_^");
        }else {
            alert('请先登录再添加购物车!')
        }
    });
    //购买量大于库存报错
    $('.product-page').on('click','.quantity-up',function () {
        var $up = $(this);
        var shuliang = Number($up.parents('.product-quantity').find('#product-quantity').val());
        var stock = Number($up.parents('.product-page-cart').siblings('.price-availability-block').find('.availability>strong').text());
        if(shuliang<stock){

        }else {
            $up.parents('.product-quantity').find('#product-quantity').val(stock);
            alert('库存量不足啊兄弟!')
        }

    });
    $('.product-page').on('click','.quantity-down',function () {
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
    var collect_status = false;
    if($('#img_collect').attr('src')=='/static/MetronicShopUI/assets/register/imgs/collectred.png'){
        collect_status = true;
    }
    function panduan(flag){//处理登录用户是否收藏该商品函数
        if(flag==true){
                      $('#img_collect').attr({'src':'/static/MetronicShopUI/assets/register/imgs/collectred.png','title':"取消收藏该商品"});
                  }else {
                      $('#img_collect').attr({'src':'/static/MetronicShopUI/assets/register/imgs/collectyellow.png','title':'点击收藏该商品'});
                  }
    }
    var count = $('.additional-nav>.pull-right>input[type=hidden]').val();
    if(count){
        $('#reviews-form').show();
    }else {
        $('#reviews-form').hide();
    }
    $('#img_collect').click(function () {
        var goods_id = $('.product-page').children('.hide_id').val();
        // console.log(count);
        if (count) {
            collect_status = !collect_status;
            $.post('collect_love',{un:count,goods_id:goods_id,collect_status:collect_status},function (data) {
                panduan(collect_status);
                $('.shoucangliang').text(data.fav_num);
            },'json');
            }else{
                alert('请先登录再进行收藏!');
        }
    });
    // 收藏爱心量点击收藏或取消

    //显示初始评论

    //显示初始评论
    //评论发表富文本
    CKEDITOR.replace('review',{
        filebrowserUploadUrl:'richtext_upload',
        toolbar :
        [
            ['Bold','Italic','Image','JustifyCenter','JustifyLeft','JustifyRight','Smiley','FontSize','TextColor']
        ]
    });
    $('.tiaofabiao').click(function () {
        var $tiao = $(this);
        if(count){
            $tiao.attr('href','#reviews-form')
        }else {
            alert('请先登录再进行评论!');
        }
    });
    $('.fabiao').click(function () {
        if (count) {
            var goods_id = $('.product-page>.hide_id').val();
            for (instance in CKEDITOR.instances){
                CKEDITOR.instances[instance].updateElement();
                }//必须加这一句后台才能收到异步提交的upload文件
                $("#reviews-form").ajaxSubmit(function (data) {
                    window.location.href = 'to_shop_item?goods_id='+goods_id
                });
            }else{
                alert('请先登录再进行评论!');
        }


    });
    //评论发表富文本
    //点击问答问题切换
    $('#Description').on('click','ul',function () {
        var $ul = $(this);
        $ul.find('li').stop().animate({
            'height':'toggle',
        })
    });
    //点击问答问题切换
    //回复
    $('#Description').on('click','.huifu',function () {
        var $req = $(this);
        if (count) {
            var Anwser = $req.next().val();
                if(Anwser==''){
                    alert('回复内容为空!')
                }else {
                    var wen_id = $req.siblings('ul').find('.hide_wen_id').val();
                    $.post('huifu',{wen_id:wen_id,Anwser:Anwser},function (data) {
                        $req.siblings('ul').find('li').remove();//先清此问题的子回复
                        $.each(data.wenda_list_this[0].fields.da,function (index,req) {
                            $req.siblings('ul').append('<li>'+req.nickname+'回复:'+req.content+'<span>'+req.da_time+'</span></li>')
                        })

                    },'json')
                }
            }else{
                alert('请先登录再进行评论!');
        }
    });
    //提问
    $('.qingwen').click(function () {
        var $ask = $(this);
        if (count) {
                var Ask = $ask.next().val();
                var goods_id = $('.product-page>.hide_id').val();
                if(Ask==''){
                    alert('提问不能为空!')
                }else {
                    $.post('qingwen',{goods_id:goods_id,Ask:Ask},function (data) {
                        $('.qingwen').before('<div class="wendada">\n' +
                            '                            <ul><em style="color: #0D47A1">'+data.wenda_list[0].fields.nickname+'</em>:'+data.wenda_list[0].fields.wen+'<strong><img src="/static/MetronicShopUI/assets/LoginImg/buzan.png" class="dianzan" alt="gg">赞'+data.wenda_list[0].fields.dianzan+'</strong><span>'+data.wenda_list[0].fields.wen_time+'</span>\n' +
                            '                                <input type="hidden" class="hide_wen_id" value="'+data.wenda_list[0].pk+'">\n' +
                            '                            </ul>\n' +
                            '                            <input type="button" class="huifu"   value="回复">\n' +
                            '                            <textarea name="Ask" class="Ask" cols="97" rows="1" ></textarea>\n' +
                            '                        </div>')
                    },'json')
                }


            }else{
                alert('请先登录再进行评论!');
        }
    });
    //点赞改数据库异步提交
    $('#Description').on('click','.dianzan',function () {
        var $zan = $(this);
        var count = $('.additional-nav>.pull-right>input[type=hidden]').val();
        var wen_id = $zan.parents('ul').find('.hide_wen_id').val();
        if(count){
            if($zan.attr('src') == '/static/MetronicShopUI/assets/LoginImg/buzan.png'){
            $.post('dianzan',{wen_id:wen_id},function (data) {
            //后台返回数据赋值点赞量
            if(data.status){
                //切换图片src
                $zan.attr('src','/static/MetronicShopUI/assets/LoginImg/zan.png');
                //切换图片src
                $zan.siblings('em').text(data.zan_num);
            }else {
                alert('不能给自己的提问点赞哦!要收敛点!')
            }
            //后台返回数据赋值点赞量
        },'json');
        }else {
            alert('您已经赞过了哦!')
        }
        }else {
            alert('请先登录再进行点赞哦')
        }


    });
    //点赞改数据库异步提交
    
    $("li>h5","#questions").bind("click",function(){
      var li=$(this).parent();
    if(li.hasClass("fold")){
      li.removeClass("fold");
      $(this).find("b").removeClass("UI-bubble").addClass("UI-ask");
      li.find(".foldContent").slideDown();
    }else{
      li.addClass("fold");
      $(this).find("b").removeClass("UI-ask").addClass("UI-bubble");
      li.find(".foldContent").slideUp();
    }
  });
    //dfgfdh
});