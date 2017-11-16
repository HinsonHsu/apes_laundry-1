/**
 * Created by H1nson on 2017/10/26.
 */
$(document).ready(function () {
    $("#btn-phone-code").click(function () {
        phone = $("#phoneNum").val()
        console.log("sended:" + phone)

        $.ajax({
            type: "POST",
            url: "/customer/code/",
            data: {phone: phone},
            dataType: 'json',
            success: function (data) {
                // $("#checkCode").val(data.code)
                console.log("receive:" + data.result);

            },
            // error: onError
        });
    });
    $("#btn-register").click(function () {
        phone = $("#phoneNum").val()
        captcha = $("#checkCode").val()
        $.ajax({
            type: "POST",
            url: "/customer/register/",
            data: {phone: phone, captcha: captcha},
            dataType: 'json',
            success: function (data) {
                console.log("receive:" + data.result);
                if(data.result == "success"){
                    location.href = "/customer/index"
                }else{
                    alert(data.errMsg)
                }
            },
            // error: onError
        })
    });
    $("#btn-login").click(function () {
        phone = $("#phoneNum").val()
        captcha = $("#checkCode").val()
        $.ajax({
            type: "POST",
            url: "/customer/login/",
            data: {phone: phone, captcha: captcha},
            dataType: 'json',
            success: function (data) {
                console.log("receive:" + data.result);
                if(data.result == "success"){
                    location.href = "/customer/index"
                }else{
                    alert(data.errMsg)
                }
            },
            // error: onError
        })
    });
})