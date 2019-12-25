$(function () {

    var my_username = $('.myusername').val();
    var fr_username;
    var fr_avatar;
    var timer;
    var qun_id;
    var items = -1;
    var myavrtar = $('.myavatar').attr('src');
    var my_nickname = $('.mynickname').text();
    // 清空所有的ckeditor的富文本编辑器
function clearCkeditor(){
    var id = "cke_chattextarea";
    var jsfunc = "";
    $(".cke_1").each(function(){
        id = $(this).attr("id");
        jsfunc = "CKEDITOR.instances."+id.substring(4)+".setData('')";
        eval(jsfunc);
    });
}
// 清空所有的ckeditor的富文本编辑器
    //点击收缩列表
    var get_news_flag=false;
    $('.haoyou').click(function () {
        get_news_flag=!get_news_flag;
        if($('.friend_item').hasClass('current')){
            $('.www').toggle(300);
        }
       $('.myfriends .friend_item').stop().animate({
           'height':'toggle',
       },200);
        if(get_news_flag){
            clearInterval(news_timer);
        }else{
            lunxun_news();
        }
    });
    $('.qunls').click(function () {
       $('.myfriends .qun_item').stop().animate({
           'height':'toggle',
       },200)
    });
    //点击收缩列表
    function serchContent(me,fr){
        $('.qun_id_hd').val('');
        if(me!=undefined&&me!=''&&fr!=undefined&&fr!=''){

            $.post('serch_content',{me:me,fr:fr},function (data) {
                if(data.status){
                    var content_obj = data.chat_list;
                if (content_obj.length!=items){    //如果信息条数增加了就刷新,不增加就不动,items头一次不能是0,否则有的聊天零记录就矛盾了,不会执行清空操作
                    items=content_obj.length;      //必须赋值下一次才会相等,不用动
                    $('.eachchat').empty();

                $.each(content_obj,function (index,chat) {
                    if (chat.send==my_username){

                        var myavatar = $('.myavatar').attr('src');
                        $('.eachchat').append('<div class="chat_item">\n' +
                            '                    <input type="hidden" class="chat_content_id" value="'+chat.num+'">\n' +
                '                    <p class="sendtime"><span>'+chat.time+'</span></p>\n' +
                '                    <img src="'+myavatar+'" class="my_pic">\n' +
                '                    <span class="my_chat">'+chat.content+'</span>\n' +
                '                </div>')
                    }else {
                        $('.eachchat').append('<div class="chat_item">\n' +
                            '                    <input type="hidden" class="chat_content_id" value="'+chat.num+'">\n' +
                            '                    <p class="sendtime"><span>'+chat.time+'</span></p>\n' +
                            '                    <img src="'+fr_avatar+'" class="fr_pic">\n' +
                            '                    <span class="fr_chat">'+chat.content+'</span>\n' +
                            '                </div>')
                    }



            });
                    $('.eachchat').scrollTop(99999);//必须在此处添加,添加完再滚动到底部
                }else {
                    console.log('已经刷新,无最新消息!')
                }
            }else {
                    alert('对方把你给删除了哈哈哈!')
                }



        },'json')




        }else {
            alert('获取失败')
        }

    }
    //发表富文本

    CKEDITOR.replace('chattextarea',{
        filebrowserUploadUrl:'rich_send_upload',
        toolbar :
        [
            ['Bold','Image','Smiley','Undo','Font','BGColor','FontSize','TextColor']
        ]
    });

    $('#sendbtn').click(function () {
        for (instance in CKEDITOR.instances){
            CKEDITOR.instances[instance].updateElement();
            }//必须加这一句后台才能收到异步提交的upload文件
        chat_addcontent();
    });
    //发表富文本

    $('.haoyou_list').on('click','.friend_item',function () {
        $('.chat_record>span').show();
        $('#fuzzysearch').val('');//代码改变值时inputproperty不能执行,点击清空输入,显示全部好友
        fuzzysearch();

        clearInterval(timer);
        items=-1;    //点击后应当把items值回归先,再刷新与其他好友的聊天记录
        $('#chattextarea').val('');
        clearCkeditor();
        $(this).addClass('current').siblings().removeClass('current');
        $('.qun_item').removeClass('current');
        $('.www').hide(300);
        fr_username = $(this).children('.frusername').val();
        serchContent(my_username,fr_username);
        timer = setInterval(function () {

            serchContent(my_username,fr_username);

        },5000);

        var fr_nickname = $(this).children('.fr_nickname').text();
        $('.cct_r>.chat_record>.current_friend').text(fr_nickname);
        fr_avatar = $(this).children('.fr_avatar').attr('src');
        $.post("click_remove_news",{my_username:my_username},function (data) {
            if(data.status){
                $.session.set('news_last',JSON.stringify(data.news_init))
            }
        },'json')

    });
    function serchQunContent(qun_id){
        $('.qun_id_hd').val(qun_id);
        if(qun_id!=undefined&&qun_id!=''){

                $.post('serch_qun_content',{qun_id:qun_id},function (data) {
                var content_obj = JSON.parse(data);
                if (content_obj.length!=items){    //如果信息条数增加了就刷新,不增加就不动,items头一次不能是0,否则有的聊天零记录就矛盾了,不会执行清空操作
                    items=content_obj.length;      //必须赋值下一次才会相等,不用动
                    $('.eachchat').empty();

                $.each(content_obj,function (index,chat) {

                    if (chat.username==my_username){
                        $('.eachchat').append('<div class="chat_item">\n' +
                '                    <input type="hidden" class="chat_content_id" value="'+chat.num+'">\n' +
                '                    <p class="sendtime"><span>'+chat.time+'</span></p>\n' +
                '                    <img src="'+chat.info+'" class="my_pic">\n' +
                '                    <span class="my_chat">'+chat.content+'</span>\n' +
                '                </div>')
                    }else {
                        $('.eachchat').append('<div class="chat_item">\n' +
                            '                    <input type="hidden" class="chat_content_id" value="'+chat.num+'">\n' +
                            '                    <p class="sendtime"><span>'+chat.time+'</span></p>\n' +
                            '                    <img src="'+chat.info+'" class="fr_pic">\n' +
                            '                    <input type="hidden" class="username_qun_hide" value="'+chat.username+'">\n' +
                            '                    <span class="fr_chat"><span>'+chat.nickname+'</span>'+chat.content+'</span>\n' +
                            '                </div>')
                    }



            });
                    $('.eachchat').scrollTop(99999);//必须在此处添加,添加完再滚动到底部
                }else {
                    console.log('已经刷新,无最新消息!')
                }


        })




        }else {
            alert('获取失败')
        }

    }
    $('.qun_list').on('click','.qun_item',function () {
        $('.current_friend').after('<p class="viewqunlist" title="查看群成员">查看&gt;&gt;&gt;</p>');
        $('.current_friend').after('<p class="yaoqing" title="邀请好友加此群">邀请&gt;&gt;&gt;</p>');
        clearInterval(timer);
        $('.chat_record>span').show();
        items=-1;    //点击后应当把items值回归先,再刷新与其他好友的聊天记录
        $('#chattextarea').val('');
        clearCkeditor();
        $(this).addClass('current').siblings().removeClass('current');
        $('.friend_item').removeClass('current');
        $('.www').hide(300);
        qun_id = $(this).children('.qun_id').val();
        serchQunContent(qun_id);
        timer = setInterval(function () {
            serchQunContent(qun_id);
        },5000);

        var qun_name = $(this).children('.qun_name').text();
        $('.cct_r>.chat_record>.current_friend').text(qun_name);



    });

    function chat_addcontent(){
        items++;//加完后发现与数据库值又一致了,不用再次清空append了,节约资源.
        var content = $('#chattextarea').val();
        var qun_id = $('.qun_id_hd').val();
        console.log('需要添加内容的群ID',qun_id);
        var space1 = content.replace('<p>','');   //去掉所有的空字符,length检测是否防护乳为空
        var space2 = space1.replace('</p>','');
        var space3 = space2.replace(/&nbsp;/g,'');
        var space = space3.replace(/ /g,'');
    if (space != ''){
        $.ajax({
            url:'chat_addcontent',
            type:'post',
            data:{send:my_username,
                myavrtar:myavrtar,
                my_nickname:my_nickname,
                receive:fr_username,
                content:content,
                qun_id:qun_id,
                },
            success:function (data) {
                //console.log(data);
                var msg = JSON.parse(data);
                $('.eachchat').append('<div class="chat_item">\n' +
            '                    <p class="sendtime"><span>'+msg.time+'</span></p>\n' +
            '                    <img src='+myavrtar+' class="my_pic">\n' +
            '                    <span class="my_chat">'+content+'</span>\n' +
            '                </div>');
                $('#chattextarea').val('');
                clearCkeditor();
                $('.eachchat').scrollTop(99999);
            },
            error:function () {
                alert('添加chat数据库失败!')
            }
        })
    }else {
        alert('输入内容为空!')
    }
    }
    $('.chat_enter').keyup(function (e) {
        if(e.ctrlKey && e.keyCode==13){   //按下ctrl+enter组合键发送
            for (instance in CKEDITOR.instances){
            CKEDITOR.instances[instance].updateElement();
            }//必须加这一句后台才能收到异步提交的upload文件
            $('#sendbtn').trigger('click');
        }
    });



    $('.search').on('click','.serch_kw_list>li',function () {
        var click_username = $(this).next().val();
        $(this).addClass('checkbg').siblings().removeClass('checkbg');//瞬间清空看不见其实
        $('.friend_item>input[value='+click_username+']').parent().trigger('click');//点击后清空输入框触发好友item点击事件

    });
    function fuzzysearch(){
        var keywords = $('#fuzzysearch').val();
        $('.serch_kw_list').empty();
        var kw_remove_space = keywords.replace(/ /g,'');
        $.post('serch_frs',{keywords:keywords},function (data) {
            var frs = JSON.parse(data);
            $('.myfriends .friend_item').remove();


            $.each(frs,function (index,fr) {


                if(fr.username!=my_username){

                        if(kw_remove_space.length>0) {//如果serch输入框内输入的不是空值的话就i
                            $('.serch_kw_list').append('<li>' + fr.nickname + '</li><input type="hidden" value="' + fr.username + '">');//搜索加li提示
                            var n=0;
                            $('.serch_kw_list>li:first').addClass('checkbg').siblings().removeClass('checkbg');
                            $('#fuzzysearch').keydown(function (event) {
                                function shangxia() {

                                    var frs_length = $('.serch_kw_list>li').length;
                                    if(n==frs_length){n=0;}
                                    else if(n==-1){n=frs_length-1;}
                                    $('.serch_kw_list>li').eq(n).addClass('checkbg').siblings().removeClass('checkbg');

                                }
                                if(event.keyCode==39||event.keyCode==40){
                                    n++;
                                    shangxia();

                                }else if(event.keyCode==37||event.keyCode==38){
                                    n--;
                                    shangxia();
                                } else if (event.keyCode==13){
                                        enter_username= $('.serch_kw_list>li[class=checkbg]').next().val();
                                        $('.friend_item>input[value='+enter_username+']').parent().trigger('click');
                                    }
                            })
                            }
                            if (fr.username != fr_username) {
                            $('.haoyou_list').append('<div class="friend_item">\n' +
                                '                <input type="hidden" value="' + fr.username + '" class="frusername">\n' +
                                '                    <img src="' + fr.info + '" class="fr_avatar">\n' +
                                '                    <span class="fr_nickname" >' + fr.nickname + '</span>\n' +
                                '                </div>')
                            } else {
                                $('.haoyou_list').append('<div class="friend_item current">\n' +
                                    '                <input type="hidden" value="' + fr.username + '" class="frusername">\n' +
                                    '                    <img src="' + fr.info + '" class="fr_avatar">\n' +
                                    '                    <span class="fr_nickname" >' + fr.nickname + '</span>\n' +
                                    '                </div>')
                            }

                }

            })

        })
    }

    $('#fuzzysearch').bind('input propertychange',function () {
       fuzzysearch();
    });
    // ***************点击头像修改************
    $('#ava_update').change(function () {
        var fr = this.files[0];
        var index = fr.name.lastIndexOf('.');
        var ext = fr.name.substring(index);//或者用.slice(m,n),不包含n
        var exts = ['.jpg','.png',',jpeg','JPEG'];
        if(exts.includes(ext)){
            if(fr.size<=4194304){
                var file = new FileReader();
                file.readAsDataURL(fr);
                file.onload=function () {
                    $('#ava_update_img').attr('src',this.result);
                };
                $('#updateAvatar').ajaxSubmit(function (data) {
                    var msg = JSON.parse(data);
                    if(msg.status){
                        alert('修改头像成功')
                    }else{
                        alert(msg.tip)
                    }
                })
            }else {
                alert('文件大小超出范围(4M)!');
            }
        }else {
            alert('输入文件格式不符合!');
        }
    });
    // ***************点击头像修改************
    // *****************点击修改昵称**************
    $('.mynickname').click(function () {
        var my_nn = prompt('确认修改昵称为下方输入框的内容?');
        var reg_nn = /^[\u4e00-\u9fa5\w]{1,10}$/;
        if(reg_nn.test(my_nn)){
                $.post('update_my_nn',{my_nn:my_nn,my_un:my_username},function (data) {
                    if(data.status){
                        $('.mynickname').text(my_nn);
                        alert('成功修改昵称')
                    }else {
                        alert('修改失败'+data.tip)
                    }
                },'json');

        }else {

            alert('修改昵称失败,格式不符合(1-10位中文或字母数字下划线)!')
        }
    });
    // *****************点击修改昵称**************
    //点击viewqunlist切换显示群成员列表
    $('.cct').on('click','.viewqunlist',function () {
        $('.this_qunlist').toggle(500);
        $('.this_qunlist').empty();
        $('.this_qunlist').append('<p style="width: 100%;height: 40px;font-size: 20px;color: white;line-height: 40px;margin: 0;">群成员列表</p>')
        $.post('search_qun_list',{qun_id:qun_id},function (data) {
            $.each(data,function (index,chengyuan) {
                $('.this_qunlist').append('<div class="friend_item">\n' +
                '        <input type="hidden" value="'+chengyuan.username+'" class="frusername">\n' +
                '        <img src="'+chengyuan.info+'" class="fr_avatar">\n' +
                '        <span class="fr_nickname" >'+chengyuan.nickname+'</span>\n' +
                '    </div>')
            })

        },'json')
    });
    //点击viewqunlist切换显示群成员列表
    //查找新朋友
    $('.chazhaouser').click(function () {
        $('.add_new_user').toggle(500);
    });
    $('.chazhaoyonghu').keyup(function (e) {
        if(e.keyCode==13){   //按下ctrl+enter组合键发送
            $('.add_new_user>a').trigger('click');
        }
    });
    $('.add_new_user>a').click(function () {
        $('.search_list').empty();//清空上次查找的;
        var search_content = $('.chazhaoyonghu').val();
        search_content = search_content.replace(/ /g,'');
        if(search_content!=''){
            $.post('search_user_list',{my_username:my_username,search_content:search_content},function (data) {
                $('.chazhaoyonghu').val('');
                console.log(data)
                if(data.length!=0){
                    $.each(data,function (index,new_fr) {

                    $('.search_list').append('<div class="friend_item">\n' +
                        '            <input type="hidden" value="'+new_fr.username+'" class="frusername">\n' +
                        '            <img src="'+new_fr.info+'" class="fr_avatar">\n' +
                        '            <span class="fr_nickname" >'+new_fr.nickname+'</span>\n' +
                        '            <a href="javascript:;" style="color: sandybrown;">添加</a>\n' +
                        '        </div>')
            })
                }else {
                    $('.search_list').append('<p>未搜索到!</p>')
                }


        },'json')
        }else {
            alert('搜索内容为空!')
        }

    });
    //查找新朋友
    //好友请求
    var get_new_fr_flag = false;
    get_new_fr();
    $('.new_fr').click(function () {
        get_new_fr_flag=!get_new_fr_flag;
        $('.new_fr_list').toggle(300);
        if(get_new_fr_flag){
            clearInterval(timer_new_fr);
        }else{
            get_new_fr();
        }

    });
    //好友请求
    //轮询新请求
    function get_new_fr() {
        timer_new_fr = setInterval(function () {

        $.post('shuaxin_new_fr',{},function (data) {
            $('.new_fr_list').empty();
            if(data.length!=0){
                $.each(data,function (index,fr) {
                    $('.new_fr_list').append('<div class="friend_item">\n' +
                        '                        <input type="hidden" value="'+fr.username+'" class="frusername">\n' +
                        '                        <img src="'+fr.info+'" class="fr_avatar">\n' +
                        '                        <span class="fr_nickname" >'+fr.nickname+'</span>\n' +
                        '                        <a href="javascript:;" class="jieshou">接受</a>\n' +
                        '                        <a href="javascript:;" class="jujue">拒绝</a>\n' +
                        '                    </div>')
                })
            }else {
                $('.new_fr_list').append('<p>暂无好友请求!</p>')
            }
        },'json')
    },20000);
    }
    //轮询新请求
    //添加新好友
    $('.search_list').on('click','a',function () {
        var $tianjia = $(this);
        var to_username = $tianjia.parent().find('.frusername').val();
        $.post('add_new_fr',{my_username:my_username,to_username:to_username},function (data) {
            if(data.status){
                alert('已成功发送申请')
            }else {
                alert('发送申请失败')
            }
        },'json')
    });
    //添加新好友
    //接受新好友请求
    $('.new_fr_list').on('click','.jieshou',function () {
        var $jieshou=$(this);
        var from_username = $jieshou.parent().find('.frusername').val();
        console.log('接受',from_username)
        $.post('jieshou_new_fr',{from_username:from_username,to_username:my_username},function (fr) {
            $jieshou.parent().remove();
            $('.haoyou_list').append('<div class="friend_item">\n' +
                                '                <input type="hidden" value="' + fr.username + '" class="frusername">\n' +
                                '                    <img src="' + fr.info + '" class="fr_avatar">\n' +
                                '                    <span class="fr_nickname" >' + fr.nickname + '</span>\n' +
                                '                </div>')

        },'json')
    });
    //接受新好友请求
    //拒绝好友请求
    $('.new_fr_list').on('click','.jujue',function () {
        var $jujue=$(this);
        var from_username = $jujue.parent().find('.frusername').val();
        $.post('jieshou_new_fr',{from_username:from_username,to_username:my_username},function (data) {
            $jujue.parent().remove();
        },'json')
    });
    //拒绝好友请求
    //删除好友或退出群
    $('.chat_record').on('click','.shanchutuichu',function () {
        var xuanze = confirm('确定删除此好友或退出此群?');
        if(xuanze){
            $.post('shanchutuichu',{my_username:my_username,qun_id:qun_id,fr_username:fr_username},function (data) {
                if(data.status){
                    window.location.href = 'to_chat';
                }
            },'json')
        }
    });
    //删除好友或退出群
    //新建群聊
    $('.xinjianqun').click(function () {
        $('.create_new_qun').toggle(500);
    });
    //新建群聊
    $('.create_new_qun>a').click(function () {
        var $create = $(this);
        var qun_nickname_space = $create.parent().find('.qun_nickname').val();
        var qun_nickname = qun_nickname_space.replace(/ /g,'');
        if (qun_nickname){
            $.post('create_qun',{qun_nickname:qun_nickname,create_user:my_username},function (data) {
                if(data.status){
                    $create.parent().find('.qun_nickname').val('');
                    alert('成功创建群聊:',data.qun_nickname);
                    window.location.href = 'to_chat';
                }else {
                    alert('创建失败!')
                }
            },'json')
        }else {
            alert('群昵称不能为空!')
        }
    });
    //邀请好友进群
    $('.chat_record').on('click','.yaoqing',function () {
        $('.yaoqing_fr').toggle(500);
        $('.yao_haoyou_list').empty();
        $.post('yaoqing_list',{qun_id:qun_id,my_username:my_username},function (data) {
            $.each(data,function (index,fr) {
                $('.yao_haoyou_list').append('<div class="friend_item">\n' +
                    '                        <input type="hidden" value="'+fr.username+'" class="frusername">\n' +
                    '                        <img src="'+fr.info+'" class="fr_avatar">\n' +
                    '                        <span class="fr_nickname" >'+fr.nickname+'</span>\n' +
                    '                        <a href="javascript:;" class="yaoqing_btn">邀请</a>\n' +
                    '                    </div>')
            })

        },'json')

    });
    $('.yaoqing_fr').on('click','.yaoqing_btn',function () {
        var $yao_btn = $(this);
        var yao_username = $yao_btn.parent().find('.frusername').val();
        $.post('yaoqing_fr',{qun_id:qun_id,yao_username:yao_username},function (data) {
            if(data.status){
                alert('成功邀请:',data.yao_username);
                $yao_btn.remove();//邀请按钮删除
            }else {
                alert('邀请失败!')
            }

        },'json')
    });
    //邀请好友进群
    var news_timer;
    var news_last = 'NO';
    function lunxun_news() {
        news_timer = setInterval(function () {
            if($.session.get("news_last")!=undefined&&$.session.get("news_last")!=''){
                news_last = $.session.get("news_last");
            }
            $.post('luxun_news',{news_last:news_last,my_username:my_username},function (data) {
                if(data.status){
                    $.each(data.new_frs,function (index,fr) {
                        $('.haoyou_list').prepend('<div class="friend_item">\n' +
                                '                <input type="hidden" value="' + fr.username + '" class="frusername">\n' +
                                '                    <img src="' + fr.info + '" class="fr_avatar">\n' +
                                '                    <span class="fr_nickname" >' + fr.nickname + '</span>\n' +
                                '                    <em style="display: inline-block;width: 24px;height: 24px;background:green;border-radius: 50%;text-align: center;line-height: 24px;color: white">新</em>\n' +
                                '                </div>')
                    })
                }else {
                    if(data.status_news){
                        console.log('到新消息了');
                        var news_compare = data.news_compare;
                        $.each(news_compare,function (key,val) {
                            if(val>0){
                                if($('.haoyou_list').find('input[value='+key+']').parent().find('em').length==0){
                                    $('.haoyou_list').find('input[value='+key+']').parent().append('<em style="display: inline-block;width: 24px;height: 24px;background:green;border-radius: 50%;text-align: center;line-height: 24px;color: white">'+val+'</em>')
                                }
                            }
                        })
                    }else {
                        $.session.set('news_last',JSON.stringify(data.news_init))
                    }
                }
            },'json')
        },15000)
    };
    lunxun_news();

});