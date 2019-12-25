$(function () {
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
                    '                                  <h3><a href="to_shop_item?good_id='+item.pk+'">'+item.fields.name+'</a></h3>\n' +
                    '                                  <div class="pi-price">'+item.fields.current_price+'</div>\n' +
                    '                                  <a href="to_shop_item?good_id='+item.pk+'" class="btn btn-default add2cart">查看细节</a>\n' +
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
        $.post('ajax_sort_search',{sort_type:sort_type,range_click:'NO',search_again_click:'NO'},function (data) {
            changecontent(data);
        },'json')
    });


    //range
    $('.price_range_btn').click(function () {
        var price_range = $('.price_range').val();
        $.post('ajax_sort_search',{price_range:price_range,range_click:'YES',search_again_click:'NO'},function (data) {
            changecontent(data);
        },'json')
    });
    //range
    //再搜索按钮
    $('.search_again_btn').click(function () {
        var search_again_cont = $('.search_again').val();
        if (search_again_cont!=''){
            $.post('ajax_sort_search',{search_again_cont:search_again_cont,search_again_click:'YES'},function (data) {
                changecontent(data);
            },'json')
        }else {
            alert('输入为空!')
        }

    });
    //再搜索按钮
    //选择框sort异步提交后台排序
    //按下页码异步提交
    $('.pagination').on('click','a',function () {
        var $page = $(this);
        var page_num = $page.attr('title');
        $.get('page_display_search',{page_num:page_num},function (data) {
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