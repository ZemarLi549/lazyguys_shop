$(function () {


    $('.logBut').click(function () {
        $('#admin_form').ajaxSubmit(function (data) {
            var msg = JSON.parse(data);
            if(msg.status){
                window.location.href = 'to_admin_index'
            }else {
                $('.wrongtip_admin').text(msg.Tip);
            }
        })
    })
});
