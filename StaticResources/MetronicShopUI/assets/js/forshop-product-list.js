$(function () {
    //按照分类展开category
    var c1='';
    var c2='';
    var c3='';
    var c4='';
    var fenlei='';
    if ($('.breadcrumb>li').length == 5){
        c1 = $('.breadcrumb>li').eq(1).text();
        c2 = $('.breadcrumb>li').eq(2).text();
        c3 = $('.breadcrumb>li').eq(3).text();
        c4 = $('.breadcrumb>li').eq(4).text();
        if(c1!=''){
            $('.list-group>li:contains('+c1+')').trigger('click');//针对打开分类列表
                if(c2!=''){
                    $('.list-group>li:contains('+c1+')').find('li:contains('+c2+')').trigger('click');
                    if(c3!=''){
                        $('.list-group>li:contains('+c1+')').find('li:contains('+c2+')').find('li:contains('+c3+')').trigger('click');
                        if(c4!=''){
                            $('.list-group>li:contains(' + c1 + ')').find('li:contains(' + c2 + ')').find('li:contains(' + c3 + ')').find('li:contains(' + c4 + ')').addClass('active');
                        }
                    }
                }
        }else if(c4!=''){
            $('.list-group>li:contains(品牌专区)').trigger('click');
            $('.list-group>li:contains(品牌专区)').find('li:contains('+c4+')').addClass('active');
        }

    }else if($('.breadcrumb>li').length == 2){   //针对首页>男士专区>>热卖
        fenlei = $('.breadcrumb>li').eq(1).text();
        var neworsale = fenlei.slice(0,2);//判断是热卖还是新品
        if(neworsale=='新品'||neworsale=='热卖'){
            $('.list-group>li:contains('+neworsale+'专区)').trigger('click');
            $('.list-group>li:contains('+neworsale+'专区)').find('li:contains('+fenlei+')').addClass('active');
        }

    }

    //按照分类展开category
    //页面上部分商品大长图随机展示底下的商品内容
    var subject =  $('.breadcrumb>li').eq(1).text();
    var random_j = parseInt(Math.random()*$('.product-list>div').length);
    var suiji_href = $('.product-list>div').eq(random_j).find('.add2cart').attr('href');
    var suiji_name = $('.product-list>div').eq(random_j).find('img').attr('alt');
    var suiji_img = $('.product-list>div').eq(random_j).find('img').attr('src');
    var suiji_price = $('.product-list>div').eq(random_j).find('.pi-price').text();
    $('.container-inner').append('<h1 style="color: saddlebrown;"><span >'+subject+'</span>'+suiji_name+'</h1>');
    $('.container-inner>em').text('¥'+suiji_price+'');

    $('.title-wrapper').css({'background':'url('+suiji_img+')',"background-size": "20%,100%"});

    $('.title-wrapper .add2cart').attr('href',suiji_href);
    //页面上部分商品大长图随机展示底下的商品内容

    //选择框sort异步提交后台排序
    function add_product(index,item) {
        $('.product-list').append('<div class="col-md-4 col-sm-6 col-xs-12">\n' +
                    '                              <div class="product-item">\n' +
                    '                                  <input type="hidden" class="hide_id" value="'+item.pk+'">\n' +
                    '                                  <div class="pi-img-wrapper">\n' +
                    '                                    <img src="'+item.fields.goods_img[0]+'" class="img-responsive" style="height: 260px;width: 240px;" alt="'+item.fields.name+'">\n' +
                    '                                    <div>\n' +
                    '                                      <a href="'+item.fields.goods_img[0]+'" class="btn btn-default fancybox-button">放大图片</a>\n' +
                    '                                      <a href="#product-pop-up" class="btn btn-default fancybox-fast-view">查看细节</a>\n' +
                    '                                    </div>\n' +
                    '                                  </div>\n' +
                    '                                  <h3><a href="to_shop_item?goods_id='+item.pk+'">'+item.fields.name+'</a></h3>\n' +
                    '                                  <div class="pi-price">'+item.fields.current_price+'</div>\n' +
                    '                                  <a href="to_shop_item?goods_id='+item.pk+'" class="btn btn-default add2cart">查看细节</a>\n' +
                    '                              </div>\n' +
                    '                      </div>');
                if (item.fields.is_sale == true){
                    $('.product-list>div').eq(index).children().append('<div class="sticker sticker-sale"></div>')
                }
                if (item.fields.is_new == true){
                    $('.product-list>div').eq(index).children().append('<div class="sticker sticker-new"></div>')
                }
    }
    function changecontent(data){
        $('.product-list').empty();
            console.log(data);
            $.each(data.ajax_list,function (index,item) {
                add_product(index,item);
            });
            //清空分页码div再重新添加
            $('.pagination').empty();
            $.each(data.all_page_list,function (ind,page) {
                if(page==1){
                    $('.pagination').append('<li><span>1</span></li>')
                }else(
                    $('.pagination').append('<li><a href="javascript:;"title="'+page+'">'+page+'</a></li>')
                )
            });
            if(data.all_page_list.length > 1){
                $('.pagination').append('<li><a href="javascript:;" title="2">&raquo;</a></li>')
            }

            //清空分页码div
    }

    $('.list-view-sorting .pull-right>.input-sm').change(function () {
        var sort_type = $('.pull-right>.input-sm>option:checked').text();
        $.post('ajax_sort',{sort_type:sort_type},function (data) {
            changecontent(data);
        },'json')
    });


    //range
    $('.price_range_btn').click(function () {
        var price_range = $('.price_range').val();
        $.post('ajax_sort',{price_range:price_range,range_click:'YES'},function (data) {
            changecontent(data);
        },'json')
    });
    //range
    //选择框sort异步提交后台排序

    //按下页码异步提交
    $('.pagination').on('click','a',function () {
        var $page = $(this);
        var page_num = $page.attr('title');
        $.get('page_display',{page_num:page_num},function (data) {
            $('.pagination').empty();
            $('.product-list').empty();
            var result = data.product_list_json;
            $.each(result.object_list,function (index,item) {
                add_product(index,item);
            });
            //对页码处理
            if (result.number>1){
                $('.pagination').append('<li><a href="javascript:;" title="'+(result.number-1)+'">&laquo;</a></li>')
            }
            $.each(data.all_page_list,function (ind,page) {
                if(page == result.number){
                    $('.pagination').append('<li><span>'+page+'</span></li>')
                }else(
                    $('.pagination').append('<li><a href="javascript:;"title="'+page+'">'+page+'</a></li>')
                )
            });
            if(result.number<data.all_page_list.length){
                $('.pagination').append('<li><a href="javascript:;" title="'+(result.number+1)+'">&raquo;</a></li>')
            }
            //对页码处理

        },'json');
    });
    //按下页码异步提交
});