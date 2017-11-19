$(document).ready(function () {
    $("#btn-phone-code").click(function () {
        phone = $("#phoneNum").val()
        if (checkMobile(phone)) {
            var countdown = 60
            var interval = setInterval(function () {
                settime()
            }, 1000)

            function settime() {
                if (countdown == 0) {
                    clearInterval(interval)
                    $("#btn-phone-code").attr("disabled", false);
                    $("#btn-phone-code").text("发送验证码");
                } else {
                    $("#btn-phone-code").attr("disabled", true);
                    $("#btn-phone-code").text("(" + countdown + ") s 重新发送");
                    countdown--;
                }
            }

            console.log("sended:" + phone)
            $.ajax({
                type: "POST",
                url: "/courier/code/",
                data: {phone: phone},
                dataType: 'json',
                success: function (data) {
                    console.log("receive:" + data.result);
                    if (data.result == "success") {

                    } else {
                        clearInterval(interval)
                        alert(data.errMsg)
                    }
                },
                // error: onError
            });
        }

    });
    $("#login-btn").click(function () {
        phone = $("#phoneNum").val()
        captcha = $("#checkCode").val()
        $.ajax({
            type: "POST",
            url: "/courier/login/",
            data: {phone: phone, code: captcha},
            dataType: 'json',
            success: function (data) {
                console.log("receive:" + data.result);
                if (data.result == "success") {
                    location.href = "/courier/index/"
                } else {
                    alert(data.errMsg)
                }
            },
            // error: onError
        })
    });
    $("#regiter-btn").click(function () {
        phone = $("#phoneNum").val()
        captcha = $("#checkCode").val()
        $.ajax({
            type: "POST",
            url: "/courier/register/",
            data: {phone: phone, code: captcha},
            dataType: 'json',
            success: function (data) {
                console.log("receive:" + data.result);
                if (data.result == "success") {
                    location.href = "/courier/upload/"
                } else {
                    alert(data.errMsg)
                }
            },
            // error: onError
        })
    });
})
function checkMobile(num) {
    if (num == "") {
        alert("手机号不能为空！");
        return false
    }
    else {
        var re = /^1\d{10}$/
        if (re.test(num)) {
            return true
        } else {
            alert("手机号格式错误！");
            return false
        }
    }
}



