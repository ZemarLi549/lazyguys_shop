$(function () {
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
            $.each(data.ajax_list,function (index,item) {
                add_product(index,item);
            });
    }
   //再搜索按钮
    $('.search_again_btn').click(function () {
        var search_again_cont = $('.search_again').val();
        if (search_again_cont!=''){
            $.post('ajax_sort_houtai',{search_again_cont:search_again_cont},function (data) {
                changecontent(data);
            },'json')
        }else {
            alert('输入为空!')
        }

    });
    //再搜索按钮
});