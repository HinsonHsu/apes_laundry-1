/**
 * Created by H1nson on 2017/10/28.
 */
$(document).ready(function () {
   $("#btn-logout").click(function () {
        $.ajax({
            type: "POST",
            url: "/customers/logout/",
            // data: {phone: phone,code:code},
            dataType: 'json',
            success: function (data) {
                console.log("receive:"+data);
            },
            // error: onError
        })
   });
});