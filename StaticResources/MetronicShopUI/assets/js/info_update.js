$(function () {
    var status2 = true;//密码符合正则性
    var status3 = true;//两次密码一致性
    var status4 = true;//昵称符合默认符合ture
    var flag_avatar = true;//头像上传验证,默认为真
    var status6 = true;//邮箱
    var status7 = true;//生日
    $('#nn_update').blur(function () {
        var conn = $(this).val();
        var regee = /^[A-Za-z\u4e00-\u9fa5]{2,6}$/;
        var rege_st = regee.test(conn);
        if (rege_st){
            status4 = true;
        }
        else {
            status4 = false;
        }
    });


    $('#pw_update1').blur(function () {
        con = $(this).val();
        var rege = /^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{6,10}$/;
        var rege_st = rege.test(con);
        if (rege_st) {
            status2 = true;
        } else {
            status2 = false;
        }
    });


    $('#pw_update2').blur(function () {
        var contt = $(this).val();
        if (contt == con) {
            status3 = true;
        } else {
            status3 = false;
        }
    });
    $('#birth_update').blur(function () {
    var contt = $(this).val();
    var rege = /^[1-9]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])$/   ;
        var rege_st = rege.test(contt);
        if (rege_st) {
            status7 = true;
        } else {
            status7 = false;
        }
});
$('#email_update').blur(function () {
    var contt = $(this).val();
    var rege = /^([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/;
        var rege_st = rege.test(contt);
        if (rege_st) {
            status6 = true;
        } else {
            status6 = false;
        }
});
// ******************注册头像预览验证**********
    $('#img_update').change(function () {
        var fr = this.files[0];
        var index = fr.name.lastIndexOf('.');
        var ext = fr.name.substring(index);//或者用.slice(m,n),不包含n
        var exts = ['.jpg','.png','.jpeg','.JPEG'];
        if(exts.includes(ext)){
            if(fr.size<=4194304){
                var file = new FileReader();
                file.readAsDataURL(fr);
                file.onload=function () {
                    $('#ava_img').attr('src',this.result);
                    $('#wrongtip_avatar_update').text('');
                    flag_avatar = true;
                }

            }else {
                $('#img_update').val('');
                $('#wrongtip_avatar_update').text('文件大小超出范围(4M)!');
                flag_avatar = false;
            }
        }else {
            $('#img_update').val('');
            $('#wrongtip_avatar_update').text('输入文件格式不符合!');
            flag_avatar = false;
        }

    });

//     ******************注册头像预览验证**********
$('#form_account input').change(function () {
    $('.wrongtip_update').text('');//重新输入时候清空cuowutishi
});
$('#btn_updata').click(function () {
 console.log(status2,status3,status4,flag_avatar,status6,status7);
 if($('.wrongtip_update').text()==''){
     if(status7){
        if(status6){
            if(status2){
                if(status3){
                    if(status4){
                        if(flag_avatar){
                            var choice1 = confirm('确认修改?');
                            if(choice1==true){
                                $('#form_account').ajaxSubmit(function (data) {
                                    var re = JSON.parse(data);
                                    if(re.status==true){
                                            window.location.href='to_standart'
                                    }else {
                                            window.location.href='to_standart'
                                    }
                                })
                            }

                        }else {
                            $('.wrongtip_update').text('上传头像文件有问题!')
                        }
                    }else {
                        $('.wrongtip_update').text('昵称格式不符合!')
                    }
                }else {
                    $('.wrongtip_update').text('两次密码输入不一致!')
                }
            }else {
                $('.wrongtip_update').text('密码格式不符合!')
            }
        }else {
            $('.wrongtip_update').text('输入邮箱格式有误!')
        }

    }else {
        $('.wrongtip_update').text('输入生日格式有误!')
    }
 }else {
     alert('输入有误,请查看顶部红色提示!');
     $('.wrongtip_update').text('');
 }
    });
//提交按钮验证

    //百度图片搜索
    var page_num = $('.page_num').val();
    if(parseInt(page_num)<=1){
        $('.pre_page').hide();
    }else{
        $('.pre_page').show();
    }

    $('.sousuo_avatar_plus').click(function () {
        $('.avatars_container').stop().toggle(200);
    });
    function ppp(data){
        $('.container_avatar_sm').empty();
        $('.container_avatar_sm').removeClass('container_avatar_sm_active')
        $('.sousuo_avatar').val(data.keyword);
            $('.page_num').val(data.page_num);
            if (data.pics_info.length==0){
                $('.yeye').hide();
                $('.container_avatar_sm').prepend('<h2>搜索结果为空!可能网速问题,可再试一下</h2>')
            }else {
                $('.yeye').show();

                $.each(data.pics_info,function (index,item) {
                    $('.container_avatar_sm').prepend('<div class="touxiang_div"><img src="'+item.pic_url+'" alt="加载失败" title="选我" class="avatar_bd"></div>');
                });
            }
    }
    $('.sousuo_btn').click(function () {
        $('.container_avatar_sm').addClass('container_avatar_sm_active')
        $('.container_avatar_sm').empty();
        var keyword = $('.sousuo_avatar').val();
        $.get('bd_spider_pic',{keyword:keyword,page_num:1},function (data) {
            ppp(data);
        },'json')
        if(parseInt($('.page_num').val())<=1){
                $('.pre_page').hide();
            }else{
                $('.pre_page').show();
            }
    });
    $('.next_page').click(function () {
        $('.container_avatar_sm').addClass('container_avatar_sm_active')
        $('.container_avatar_sm').empty();
        page_num = parseInt($('.page_num').val())+1;
        $('.page_num').val(page_num);
        var keyword = $('.sousuo_avatar').val();
        $.get('bd_spider_pic',{keyword:keyword,page_num:page_num},function (data) {
            ppp(data);
        },'json');
        if(page_num<=1){
            $('.pre_page').hide();
        }else{
            $('.pre_page').show();
        }
    });
    $('.pre_page').click(function () {
        $('.container_avatar_sm').addClass('container_avatar_sm_active')
        $('.container_avatar_sm').empty();
        page_num = parseInt($('.page_num').val())-1;
        $('.page_num').val(page_num);
        var keyword = $('.sousuo_avatar').val();
        $.get('bd_spider_pic',{keyword:keyword,page_num:page_num},function (data) {
            ppp(data);
        },'json');
        if(page_num<=1){
            $('.pre_page').hide();
        }else{
            $('.pre_page').show();
        }
    });
    $('.sousuo_avatar').keyup(function (e) {
        if(e.keyCode==13){
            $('.sousuo_btn').trigger('click');
        }
    });
    $('.page_num').keyup(function (e) {
        if(e.keyCode==13){
            $('.container_avatar_sm').addClass('container_avatar_sm_active')
            $('.container_avatar_sm').empty();
            page_num = $('.page_num').val();
            var keyword = $('.sousuo_avatar').val();
            $.get('bd_spider_pic',{keyword:keyword,page_num:page_num},function (data) {
                ppp(data);
            },'json');
            if(parseInt($('.page_num').val())<=1){
                $('.pre_page').hide();
            }else{
                $('.pre_page').show();
            }
        }
    });
    $('.container_avatar_sm').on('click','.touxiang_div>img',function () {
        $(this).toggleClass('fangda').parent().siblings().find('img').removeClass('fangda');
    });
    $('.xuanze_avatar').click(function () {
        var tu_url = $('.fangda').attr('src');
        $.get('xuanze_avatar',{tu_url:tu_url},function (data) {
            if(data.status){
                alert('修改头像成功')
                window.location.href = 'to_standart'
            }else {
                alert('修改失败!')
            }
        },'json')
    })
});
