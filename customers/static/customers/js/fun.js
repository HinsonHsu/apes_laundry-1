//
// /**
//  * Created by H1nson on 2017/10/28.
//  */
// function jump() {
//     window.open("");
// }
//
// function jump_user_log() { //个人中心更多中的退出登录按钮跳转
//     window.location.href = 'personal_center.html';
// }
// //检测手机号码是否正确 并发验证码
// function verify_phone(obj) {
//     var phone = document.getElementById("inputValue").value;
//     var reg0 = /^13\d{5,9}$/; //130--139。至少7位
//     var reg1 = /^153\d{8}$/; //联通153。至少7位
//     var reg2 = /^159\d{8}$/; //移动159。至少7位
//     var reg3 = /^158\d{8}$/;
//     var reg4 = /^150\d{8}$/;
//     var my = false;
//     if (reg0.test(phone)) {
//         my = true;
//     }
//     if (reg1.test(phone)) {
//         my = true;
//     }
//     if (reg2.test(phone)) {
//         my = true;
//     }
//     if (reg3.test(phone)) {
//         my = true;
//     }
//     if (reg4.test(phone)) {
//         my = true;
//     }
//     if (!my) {
//         alert('对不起，您输入的手机号码错误。')
//     } else {
//         var countdown = 60;
//         settime(obj);
//
//         function settime(obj) {
//             if (countdown == 0) {
//                 $(obj).attr("disabled", false);
//                 $(obj).text("发送验证码");
//                 countdown = 60;
//                 return;
//             } else {
//                 $(obj).attr("disabled", true);
//                 $(obj).text("(" + countdown + ") s 重新发送");
//                 countdown--;
//             }
//             setTimeout(function () {
//                 settime(obj)
//             }, 1000)
//         }
//     }
// }
// ////检测邮箱并发验证码   //目前问题：检测不完全
// // function verify_email(email_address) {
// //     var regex = /^([0-9A-Za-z\-_\.]+)@([0-9a-z]+\.[a-z]{2,3}(\.[a-z]{2})?)$/g;
// //     if ( regex.test( email_address ) )
// //     {
// //         var countdown = 60;
// //         settime( email_address);
//
// //         function settime( email_address) {
// //             if (countdown == 0) {
// //                 $( email_address).attr("disabled", false);
// //                 $( email_address).text("发送验证码");
// //                 countdown = 60;
// //                 return;
// //             } else {
// //                 $( email_address).attr("disabled", true);
// //                 $( email_address).text("(" + countdown + ") s 重新发送");
// //                 countdown--;
// //             }
// //             setTimeout(function () {
// //                 settime( email_address)
// //             }, 1000)
// //         }
// //         return true;
// //     }
// //     else
// //     {
//
// //         window.alert( "您输入的电子邮件地址不合法" );
// //         return false;
//
//
//
// //     }
// // }
//
// $(document).on('click','#email_address',function(){
//     isEmail($(this));
// })
// function isEmail($obj){
//     var countdown = 60;
//     var regex = /^([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+@([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+\.[a-zA-Z]{2,3}$/;
//     if ( regex.test( $('#emaill').val() ) )
//     {
//         settime($obj);
//
//         setInterval(function () {
//             settime($obj)
//         }, 1000)
//     }
//     else{
//         window.alert( "您输入的电子邮件地址不合法" );
//     }
//     function settime($o) {
//         if (countdown == 0) {
//             $o.attr("disabled", false);
//             $o.text("发送验证码");
//             countdown = 60;
//             return;
//         } else {
//             $o.attr("disabled", true);
//             $o.text("(" + countdown + ") s 重新发送");
//             countdown--;
//         }
//     }
// }
//
//
// function verify_change_code() {    // 不能检测出不一样
//     var password = $('#password').val();
//     var repassword = $('#repassword').val();
//     if(password !==repassword){
//         alert ('新旧密码不一样');
//     }
//     else{
//        window.location.href = 'enterprise_log.html';
//     }
// }
// // if(success){
// //     var phone = $('#').val();
// //     window.location.href('www.baidu.com?phone=' + phone);
// //     window.location.href('www.baidu.com?phone=111');
// // }
//
// // function getUrlPara(name){
// //     return value;
// // }
//
// // $().val()
//
// // $.ajax({
// //     success:functon(data){
// //         data{}
// //     }
// // })
function validatemobile(mobile) {
    if (mobile.length == 0) {
        alert('请输入手机号码！');
        return false;
    }
    if (mobile.length != 11) {
        alert('请输入有效的手机号码！');
        return false;
    }

    var reg = /^1[3|4|5|8][0-9]\d{4,8}$/
    if (!reg.test(mobile)) {
        alert('请输入有效的手机号码！');
        return false;
    }
}
function validatecode(captcha) {
    if (captcha.length != 4) {
        alert('请输入有效的验证码！');
        return false;
    }
}
$(document).ready(function () {
    $("#btn_phone").click(function () {
        phone = $("#phoneNum").val()
        if (validatemobile(phone) == false) {
            return false
        }
        var countdown = 60
        var interval = setInterval(function () {
            settime()
        }, 1000)

        function settime() {
            if (countdown == 0) {
                clearInterval(interval)
                $("#btn_phone").attr("disabled", false);
                $("#btn_phone").text("发送验证码");
            } else {
                $("#btn_phone").attr("disabled", true);
                $("#btn_phone").text("(" + countdown + ")s重新发送");
                countdown--;
            }
        }

        console.log("sended:" + phone)
        $.ajax({
            type: "POST",
            url: "/customer/code/",
            data: {phone: phone},
            dataType: 'json',
            success: function (data) {
                // $("#checkCode").val(data.code)
                if (data.result == "success") {
                    console.log("res:" + data.result)
                } else {
                    clearInterval(interval)
                    alert(data.errMsg)
                }

            },
            // error: onError
        });
    })
    $("#btn-login").click(function () {
        phone = $("#phoneNum").val()
        code = $("#checkCode").val()
        if (validatemobile(phone) == false || validatecode(code) == false) {
            return false
        }
        console.log("logining..,")
        $.ajax({
            type: "POST",
            url: "/customer/login/",
            data: {phone: phone, code: code},
            dataType: 'json',
            success: function (data) {
                console.log("receive:" + data.result);
                if (data.result == "success") {
                    location.href = "/customer/index"
                } else {
                    alert(data.errMsg)
                }
            },
            // error: onError
        })
    });
    $("#btn-register").click(function () {
        phone = $("#phoneNum").val()
        code = $("#checkCode").val()
        $.ajax({
            type: "POST",
            url: "/customer/register/",
            data: {phone: phone, code: code},
            dataType: 'json',
            success: function (data) {
                console.log("receive:" + data.result);
                if (data.result == "success") {
                    location.href = "/customer/index"
                } else {
                    alert(data.errMsg)
                }
            },
            // error: onError
        })
    });
});