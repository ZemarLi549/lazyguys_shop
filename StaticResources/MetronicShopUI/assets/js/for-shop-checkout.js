$(function () {
    var status1 = false;//手机号是否符合正则
    var status2 = false;//地址是否为空
    var status3 = false;//收货人姓名否为空是
    //初始化格式问题
    $('#shipping-address .accordion-toggle').trigger('click');//初始打开第一步
    $('#button-shipping-address').click(function () {
        $('#shipping-address .accordion-toggle').trigger('click');
    });
    $('#button-shipping-method').click(function () {
        $('#shipping-method .accordion-toggle').trigger('click');
    });
    $('#button-payment-method').click(function () {
        $('#payment-method .accordion-toggle').trigger('click');
    });
    //初始化格式问题
    //处理错误
    $('#order_form input').on('input propertychange',function () {
        $('.wrongtip_order').text('');
    });
    $('#button-confirm').click(function () {
        if($('.wrongtip_order').text()!=''){//处理错误
            $('.wrongtip_order').text('');
            alert('请查看底部的红色错误提示!');//处理错误

        }

        //清空session购物车
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
        var cart_goods_ls=[];
                $.session.set("cart_goods_ls",'');
                cart_add(cart_goods_ls);
                $('.top-cart-info-count>span').text(0);
        //清空session购物车

        //详细地址是否为空
        var add_detail = $('#add_detail').val();
        var province = $('#province').val();
        var city = $('#city').val();
        var town = $('#town').val();
        if (add_detail!=''&&province!=''&&city!=''&&town!=''){
            status2=true;
        }else {
            status2=false;//地址是否为空
        }
        //详细地址是否为空
        //手机号是否符合
        var cont = $('#telephone-dd').val();
            var reg = /^1[34578]\d{9}$/;
            var reg_st = reg.test(cont);
            if (reg_st){
                status1 = true;
            }
            else {
                status1 = false;
            }
        //手机号是否符合
        //姓名是否为空
        var name = $('#name-dd').val();
        if (name!=''){
            status3=true;
        }else {
            status3=false;
        }
        //姓名是否为空
        if(status1){
            if(status3){
                if(status2){
                $('#order_form').ajaxSubmit(function (data) {
                    var msg = JSON.parse(data);
                    if(msg.status){
                            window.location.href = msg.re_url;
                    }else {
                        window.location.href = 'to_pay_page';
                    }
                });
                }else {
                    $('.wrongtip_order').text('收获地址不够完善!')
                }
            }else {
                $('.wrongtip_order').text('收货人姓名不能为空!')
            }
        }else {
            $('.wrongtip_order').text('手机号输入有误!')
        }
    });
    //点击选择常用地址
    $('.changyong').on('click','.add_info',function () {
       var $div = $(this);
       $div.addClass('dizhiactive').siblings().removeClass('dizhiactive');
       var signer_name = $div.find('.xingming').text();
       var signer_mobile = $div.find('.dianhua').text();
       var province = $div.find('.sheng').text();
       var city = $div.find('.shi').text();
       var district = $div.find('.xian').text();
       var address = $div.find('.xiangxi').text();
       console.log(city,district)
       $('#name-dd').val(signer_name);
       $('#telephone-dd').val(signer_mobile);
       $('#province').find('option:contains('+province+')').prop('selected',true);
       $('#province').trigger('change');//必须得加此动作!
       $('#city').find('option:contains('+city+')').prop('selected',true);
       $('#city').trigger('change');
       $('#town').find('option:contains('+district+')').prop('selected',true);
       $('#add_detail').val(address);
    });
    $('#shipping-address-content input').change(function () {
        $('.add_info').removeClass('dizhiactive');
    });
    //点击选择常用地址


    //省市县三级联动
    var province= $('#province');

    var city= $('#city');

    var town= $('#town');
    $.each(provinceList,function (index,sheng) {
        province.append('<option>'+sheng.name+'</option>');
    });

    function clear(ele,val) {
        ele.empty();
        ele.append('<option>--请选择'+val+'--</option>')

    }
    function tianjia(ele,val) {
        ele.append('<option>'+val+'</option>')
    }
    var pro_index = 0;
    province.change(function () {
        clear(city,'城市');
        clear(town,'县区');
        var province_val = $(this).val();
        $.each(provinceList,function (i,pro) {
            if (pro.name == province_val) {
                pro_index = i;
                $.each(pro.cityList, function (ind,item) {
                    tianjia(city,item.name);
                });
                return false;
            }
        })
    });
    city.change(function () {
        clear(town,'县区');
        var city_val = $(this).val();
        $.each( provinceList[pro_index].cityList,function (index,city) {
            if (city_val == city.name) {
                $.each(city.areaList,function (ind,item) {
                    tianjia(town,item);
                });
                return false;
            }
        } )
    })
    //省市县三级联动

});