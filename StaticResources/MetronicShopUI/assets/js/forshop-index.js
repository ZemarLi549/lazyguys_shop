$(function () {
    var lunbo_list = JSON.parse( $('.lunbo_list').val() );
    // console.log(lunbo_list);首页7张轮播图自动播放
    $('.carousel-item-four h2>strong').text(lunbo_list[0].fields.name);
    $('.carousel-item-four h2>span').text('仅售'+lunbo_list[1].fields.current_price);
    $('.carousel-item-four .carousel-subtitle-v2').text(lunbo_list[0].fields.goods_brief);
    $('.carousel-item-five h2').text(lunbo_list[1].fields.name);
    $('.carousel-item-five .carousel-subtitle-v2').text(lunbo_list[1].fields.goods_brief);
    $('.carousel-item-five .carousel-subtitle-v3').text('特价甩卖'+lunbo_list[1].fields.current_price);
    $('.carousel-item-six .yi').text(lunbo_list[2].fields.name);
    $('.carousel-item-six .carousel-subtitle-v4').text('下单享8折'+lunbo_list[2].fields.current_price);
    $('.carousel-item-six .er').text(lunbo_list[2].fields.goods_brief);
    $('.carousel-item-seven h2').text(lunbo_list[3].fields.category_yi+'   '+lunbo_list[3].fields.name);
    // $('.carousel-item-four').attr('style','background: url('+lunbo_list[0].fields.goods_img[0]+');background-size:cover;');
    // $('.carousel-item-five').attr('style','background: url('+lunbo_list[1].fields.goods_img[0]+');background-size:cover;');
    // $('.carousel-item-six').attr('style','background: url('+lunbo_list[2].fields.goods_img[0]+');background-size:cover;');
    // $('.carousel-item-seven').attr('style','background: url('+lunbo_list[3].fields.goods_img[0]+');background-size:cover;');
    $('.lunbo_small_1').attr('src',lunbo_list[4].fields.goods_img[0]);
    $('.lunbo_small_2').attr('src',lunbo_list[5].fields.goods_img[0]);
    $('.lunbo_small_3').attr('src',lunbo_list[6].fields.goods_img[0]);
//*****************大长图自动轮播*********
            autoplay_carousel();
            function autoplay_carousel() {
                timer_carousel = setInterval(function () {
                $('#carousel-example-generic .fa-angle-right').trigger('click')
            },6000);
            }

            $('.page-slider').hover(function () {
                clearInterval(timer_carousel);
            },function () {
                autoplay_carousel();
            });
            //*****************大长图自动轮播*********


});