$(function () {
    //立即登录按钮异步提交
    $('#form1 input').bind('input propertychange',function () {
        $('.wrongtip').text('');//重新输入时候清空cuowutishi
    });
    $('#form2 input').bind('input propertychange',function () {
        $('.wrongtip_msg').text('');//重新输入时候清空cuowutishi
    });
    $('#jsLoginBtn').click(function () {
        //清空session购物车
        $.session.set("cart_goods_ls",'');
    //清空session购物车
        if($('.wrongtip').text()!=''){
            alert('请输入正确用户名密码和验证码!');
            $('.wrongtip').text('');
        }else {
            $('#form1').ajaxSubmit(function (data) {
            var msg_obj= JSON.parse(data);
            if (msg_obj.status){
                console.log('登陆成功');
                window.location.href='/'
            }else{
                $('.wrongtip').text(msg_obj.Tip);
            }
        });
        }


    });
    //立即登录按钮异步提交
    $('.fr').click(function () {
        $('#inner').trigger('click');
    });
    //短信验证登录
    $('#jsLoginBtn2').click(function () {
            //清空session购物车
            $.session.set("cart_goods_ls",'');
            //清空session购物车
            if($('.wrongtip_msg').text()!=''){
                alert('请检查手机号和验证码或网络断开!');
                $('.wrongtip_msg').text('');
            }else {
                $('#form2').ajaxSubmit(function (data) {
                var msg_obj= JSON.parse(data);
                if (msg_obj.status){
                    console.log('登陆成功');
                    window.location.href='/'
                }else{
                    $('.wrongtip_msg').text(msg_obj.tips);
                }
            });
            }


        });
    //短信验证登录
    //focus输入框样式改变
    $('.tab-form input').focus(function () {
        $(this).addClass('input-focus')
    });
    $('.tab-form input').blur(function () {
        $(this).removeClass('input-focus')
    });
    //focus输入框样式改变
    //动态登录滑动开关切换
    document.getElementById("inner").onclick = function() {
			if (this.className == "inner-on") {
				this.style.left = -90 + "px";
				this.childNodes[1].checked = false;
				this.className = "inner-off";

			}else{
				this.style.left = 0;
				this.childNodes[1].checked = true;
				this.className = "inner-on";
			}
			$('.tab-form').animate({
                "height":"toggle",
                "width":"toggle",
            },500)
		};
    //动态登录切换
    //短信验证码倒计时
    $('#codebtn2').click(function () {
        if($('.wrongtip_msg').text()!=''){
                alert('请检查手机号!');
                $('.wrongtip_msg').text('');
        }else {
            //提交后台制作验证码
            var username = $('#phone_f2').val();
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
                $('.wrongtip_msg').text(data.tips)
            }
        },'json');
        //提交后台验证
        }



    });

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
});