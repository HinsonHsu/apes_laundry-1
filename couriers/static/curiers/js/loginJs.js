$(document).ready(function () {
    $("#btn-phone-code").click(function () {
        phone = $("#phoneNum").val()
        console.log("sended:" + phone)

        $.ajax({
            type: "POST",
            url: "/courier/code/",
            data: {phone: phone},
            dataType: 'json',
            success: function (data) {
                $("#checkCode").val(data.code)
                console.log("receive:" + data.result);

            },
            // error: onError
        });
    });
    $("#regiter-btn").click(function () {
        phone = $("#phoneNum").val()
        captcha = $("#checkCode").val()
        $.ajax({
            type: "POST",
            url: "/courier/register/",
            data: {phone: phone, captcha: captcha},
            dataType: 'json',
            success: function (data) {
                console.log("receive:" + data.result);
                if (data.result == "success") {
                    location.href = "/courier/register/"
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
    }
    else {
        var re = /^1\d{10}$/
        if (re.test(num)) {
            alert("验证码已发送");
            var countdown = 60
            var interval = setInterval(function () {
                settime()
            }, 1000)
            function settime() {
                if (countdown == 0) {
                    clearInterval(interval)
                    $("#btn_verification_code").attr("disabled", false);
                    $("#btn_verification_code").text("发送验证码");
                } else {
                    $("#btn_verification_code").attr("disabled", true);
                    $("#btn_verification_code").text("(" + countdown + ") s 重新发送");
                    countdown--;
                }
            }

            $.ajax({
                type: "POST",
                url: "/courier/code/",
                data: {phone: num},
                dataType: 'json',
                success: function (data) {
                    // $("#checkCode").val(data.code)
                    console.log("receive:" + data.result);

                },
                // error: onError
            });
        } else {
            alert("手机号格式错误！");
        }
    }
}



