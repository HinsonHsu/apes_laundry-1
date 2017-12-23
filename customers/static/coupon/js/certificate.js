$(document).ready(function () {

})
var cdkey = null;
function moneyChanged(val) {
    cdkey = val
}
function onCertificate() {
    $.ajax({
        type: "POST",
        url: "/customer/certificate/",
        data: {'cdkey': cdkey},
        dataType: 'json',
        success: function (data) {
            // $("#checkCode").val(data.code)
            console.log("receive:" + data.code);
            if (data.code == 0) {
                alert('兑换成功!')
            } else {
                alert('兑换失败:'+data.errMsg);
            }
        },
        // error: onError
    });
}