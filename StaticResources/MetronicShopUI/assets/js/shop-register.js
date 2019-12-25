$(function () {

        var status1 = false;//用户名是否重名
        var status5 = false;//用户名是否符合正则
        var status4 = true;//昵称符合默认符合ture
        var status3 = false;//两次密码一致性
        var status2 = false;//密码符合正则性
        var flag_avatar = true;//头像上传验证,默认为真
        $('#un').blur(function () {
            var cont = $(this).val();
            var reg = /^1[3456789]\d{9}$/;
            var reg_st = reg.test(cont);
            $('#un_status').attr('src','/static/MetronicShopUI/assets/register/imgs/loading.gif').show();
            if (reg_st){
                status5 = true;
                $.post('check_un',{register_form:cont},function (data) {
                    if(data.status){
                        status1 = true;
                        setTimeout(function () {
                            $('#un_status').attr('src','/static/MetronicShopUI/assets/register/imgs/right.jpg');
                        },300);

                    }else {
                        status1 = false;
                        setTimeout(function () {
                            $('#un_status').attr('src','/static/MetronicShopUI/assets/register/imgs/cha.jpg');
                        },300)

                    }
                },'json')
            }
            else {
                status5 = false;
                setTimeout(function () {
                    $('#un_status').attr('src','/static/MetronicShopUI/assets/register/imgs/cha.jpg');
                },300)
            }

        });



    $('#pw').blur(function () {
        con = $(this).val();
        var rege = /^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{6,12}$/;
        var rege_st = rege.test(con);
        $('#psw_status').attr('src','/static/MetronicShopUI/assets/register/imgs/loading.gif').show();
        if (rege_st){
            status2 = true;
            setTimeout(function () {
                $('#psw_status').attr('src','/static/MetronicShopUI/assets/register/imgs/right.jpg');
            },300);
        }
        else {
            setTimeout(function () {
                $('#psw_status').attr('src','/static/MetronicShopUI/assets/register/imgs/cha.jpg');
            },300);
            status2 = false;

        }
    });
    //密码难度显示
    $('#pw').bind('input propertychange', function () {
        var psw_shishi = $(this).val();
        var psw_len = psw_shishi.length;
        var re_purenum = /^[\d]{0,12}$/;//不能纯数字字母简单
        if (!re_purenum.test(psw_shishi)) {
            // console.log('难')
            $('#pswnandu').width(5 + psw_len * 30);
        } else {
            // console.log('简单')
            $('#pswnandu').width(5 + psw_len * 15);
        }
    });
    //密码难度显示
    $('#verify_pw').blur(function () {
        var contt = $(this).val();
        $('#psw_verify_status').attr('src','/static/MetronicShopUI/assets/register/imgs/loading.gif').show();
        if (con==''){
            status3 = false;
            $('#psw_verify_status').attr('src','/static/MetronicShopUI/assets/register/imgs/cha.jpg');
        }else {
            if (contt==con){
            status3 = true;
            $('#psw_verify_status').attr('src','/static/MetronicShopUI/assets/register/imgs/right.jpg');
        }
        else {
            status3 = false;
            $('#psw_verify_status').attr('src','/static/MetronicShopUI/assets/register/imgs/cha.jpg');
        }
        }

    });
    $('#nn').blur(function () {
        var conn = $(this).val();
        $('#nn_status').attr('src','/static/MetronicShopUI/assets/register/imgs/loading.gif').show();
        var regee = /^[A-Za-z\u4e00-\u9fa5]{2,6}$/;
        var rege_st = regee.test(conn);
        if (rege_st){
            status4 = true;
            $('#nn_status').attr('src','/static/MetronicShopUI/assets/register/imgs/right.jpg');
        }
        else {
            status4 = false;
            $('#nn').attr('src','/static/MetronicShopUI/assets/register/imgs/cha.jpg');
        }
    });
    

    //筛子昵称
    function pro(){
           var chars = '上官燕赵司马Q风W雨E黑T飞H酷炫A林志玲G胡歌F彭于晏V卢本伟M位宁辉N大小空路飞索隆山治娜美乌索普鸣人佐助泉水新一雷电卡卡罗特蒙奇思涵';
           var nn_len = parseInt(Math.random()*5+2);//2-6位(*(m-n+1)+n)
           var nn = '';
           for (let i = 0; i < nn_len ; i++) {
               var cl = chars.length;
               var j = parseInt(Math.random()*cl);
               nn += chars.charAt(j);
           }
           $('#nn').val(nn);
       }
       pro();
       $('#s').click(function () {
           var $s = $(this);
           $s.attr('src','/static/MetronicShopUI/assets/register/imgs/s.gif');
           setTimeout(function(){
               var ttt = parseInt(Math.random()*6);
               var shaizisrc =  '/static/MetronicShopUI/assets/register/imgs/s'+ttt+'.png';
               $s.attr('src',shaizisrc);
               pro();
           },800)

       });
    //筛子昵称



    //focus输入框样式改变
    $('.tab-form input').focus(function () {
        $(this).addClass('input-focus')
    });
    $('.tab-form input').blur(function () {
        $(this).removeClass('input-focus')
    });
    //focus输入框样式改变
    //轮播图
    var newimg = $('#ul>li').first().clone();
        $('.slide').mouseover(function () {
            clearInterval(timer);
            $('.unslider-arrow').show();
        }).mouseout(function () {
            $('.unslider-arrow').hide();
            autoplay();
        });
        var index = 0;
        $('#ul').append(newimg);
        var len = $('#ul>li').length;
        var wid = $('#ul>li').width();
        var hh = $('#ul>li').height();
        $('#ul').width( len*wid );
        $('#ul').height( hh);

        $('#ol>li').click(function () {
            if(index==len-1&&$(this).index()==0){
                index=len-1;
            }else {
                index=$(this).index();
            }
            play();
        });


        function play() {
            if(index==len-1){
            $('#ol>li').eq(0).addClass('bg').siblings().removeClass('bg');
        }else {
            $('#ol>li').eq(index).addClass('bg').siblings().removeClass('bg');
        }

            if(index==len){
                $('#ul').css('left','0px');
                index=1;
            }
            if(index==-1){
                $('#ul').css('left',(len-1)*-wid+'px');
                index=len-2;
            }
            $('#ul').stop().animate({'left':index*-wid},800)

        }
        function autoplay() {
            timer = setInterval(function () {
                index++;
                play();
            },4000)
        }
        autoplay();
        $('#prev').click(function () {
            index--;
            play()
        });
        $('#next').click(function () {
            index++;
            play()
        });

    //轮播图
    $('#codebtn2').click(function () {
        if($('.wrongtip').text()!=''){
            alert('请输入正确手机号!');
            $('.wrongtip').text('');
        }else {
            //提交后台制作验证码
            var username = $('#un').val();
            $.post('msg_code_make',{username:username},function (data) {
            if(data.status){
                //短信验证码倒计时
                $('#codebtn2').hide();
                var i = 60;
                var $codebtn = $('#codebtn');
                $codebtn.show();
                $codebtn.text(i);
                timerinterval=setInterval(function () {
                    i--;
                    $codebtn.text(i);
                    if(i<=0){
                    clearInterval(timerinterval);
                }
                },1000);

                timerout1 = setTimeout(function () {
                    $codebtn.hide();
                    $('#codebtn2').show();
                    $('#codebtn2').text('重新发送');
                },60000);
            }else {
                $('.wrongtip').text(data.tips)
            }
        },'json');
        //提交后台验证
        }


    });
    //短信验证码倒计时

    //提交按钮验证

$('#reg_form input').bind('input propertychange',function () {
    $('.wrongtip').text('');//重新输入时候清空cuowutishi
});
$('#regbtn').click(function () {
    //清空session购物车
        $.session.set("cart_goods_ls",'');
        //清空session购物车
    if($('.wrongtip').text()!=''){
                alert('请检查手机号和验证码!');
                $('.wrongtip').text('');
        }else{

            if(status5){
            if(status1){
                if(status2){
                    if(status3){
                        if(status4){
                            if(flag_avatar){
                                $('#reg_form').ajaxSubmit(function (data) {
                                    var re = JSON.parse(data);
                                    if(re.status==true){
                                        var choice1 = confirm('免登录进入商城主页?');
                                        if(choice1==true){
                                            window.location.href='/'
                                        }else {
                                            window.location.href='to_login'
                                        }
                                    }else {
                                        $('.wrongtip').text(re.tips)
                                    }
                                })
                            }else {
                                $('.wrongtip').text('上传头像文件有问题!')
                            }
                        }else {
                            $('.wrongtip').text('昵称格式不符合!')
                        }
                    }else {
                        $('.wrongtip').text('两次密码输入不一致!')
                    }
                }else {
                    $('.wrongtip').text('密码格式不符合!')
                }
            }else {
                $('.wrongtip').text('用户名已注册,请重输或者直接登录!')
            }

        }else {
            $('.wrongtip').text('用户名格式不符合!')
    }
    }




    });
//提交按钮验证
});
