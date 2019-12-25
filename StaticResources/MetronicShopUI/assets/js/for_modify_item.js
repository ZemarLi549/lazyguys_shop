$(function () {
    // ******************注册头像预览验证**********

    function yulan(fr,tu) {
        var index = fr.name.lastIndexOf('.');
        var ext = fr.name.substring(index);//或者用.slice(m,n),不包含n
        var exts = ['.jpg', '.png', '.jpeg', '.JPEG'];
        if (exts.includes(ext)) {
            if (fr.size <= 4194304) {
                var file = new FileReader();
                file.readAsDataURL(fr);
                file.onload = function () {
                    $('.' + tu + '').attr('src', this.result);
                    $('#wrongtip_update').text('');
                }

            } else {

                $('#wrongtip_update').text('' + tu + '文件大小超出范围(4M)!');
            }
        } else {

            $('#wrongtip_update').text('' + tu + '输入文件格式不符合!');
        }
    }

    $('#tu1').change(function () {
        $('#wrongtip_update').text('');
        var fr1 = this.files[0];
        yulan(fr1,'futu1');

    });
    $('#tu2').change(function () {
        $('#wrongtip_update').text('');
        var fr2 = this.files[0];
        yulan(fr2,'futu2');

    });
    $('#tu3').change(function () {
        $('#wrongtip_update').text('');
        var fr3 = this.files[0];
        yulan(fr3,'futu3');

    });

//     ******************注册头像预览验证**********
    $('.baocunxiugai').click(function () {
        var tt = $('#wrongtip_update').text();
        if (tt=='') {
            var queding = confirm('确定修改?');
            if(queding){
                $('#form_update').ajaxSubmit(function (data) {
                    var msg = JSON.parse(data);
                    if(msg.status){
                        alert('修改成功!');
                    }else {
                        alert('修改失败!')
                    }
                })
            }

        }else {
            alert(tt);
            $('#wrongtip_update').text('');
        }

    });
    $('.shanchugood').click(function () {
        var tt = confirm('确定删除此商品?请慎重!');
        if (tt){
            var goods_id = $('.hide_id').val();
            $.post('del_good',{goods_id:goods_id},function (data) {
                if(data.status){
                    alert('删除成功!')
                }else {
                    alert('删除失败!')
                }
            },'json')
        }
    });
    $('.addgood').click(function () {
        $.post('add_good',function (data) {
            if(data.status){
                alert('创建新商品成功!可去列表中最底下一行修改信息!');
                window.location.href='to_modify_goods'
            }else {
                alert('创建失败!')
            }
        },'json')
    });
    $('#Description').on('click','.del_tiwen',function () {
        var $del_ask = $(this);
        var ask_id = $del_ask.find('.hide_wen_id').val();
        console.log(ask_id);
        $.post('del_wenda',{ask_id:ask_id},function (data) {
            if(data.status){
                alert('删除此问答成功!')

            }else {
                alert('删除此问答失败!')
            }
        },'json')
    });
    $('.add_reviews').on('click','.del_review',function () {
        var $del_reviews = $(this);
        var review_id = $del_reviews.find('.hide_review_id').val();
        $.post('del_review',{review_id:review_id},function (data) {
            if(data.status){
                alert('删除此评论成功!')

            }else {
                alert('删除此评论失败!')
            }
        },'json')
    });


});