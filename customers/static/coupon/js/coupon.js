$(document).ready(function () {
    unuse();
})

function unuse() {
    $('.coupon').empty();
    var unuse_data = coupons.unUseCouponList;
    $.each(unuse_data, function (i, data) {
        var $item = $('<div class="stamp stamp04"><div class="par"> <sub class="sign">' + "￥" + '</sub><span>' + data.face_value + '</span><p>优惠券</p><p>订单满' + data.lump_sum +
            '元</p> </div><div class="copy">副券<p>' + data.start_time + '<br>' + data.end_time + '</p></div><i></i></div>');
        $item.appendTo($('.coupon'));
    })
    // $.each(unuse_data.data2, function (i, data) {
    //     var $item = $('<div class="stamp stamp04"><div class="par"><span>' + data.face_value + '</span></div><div class="copy">副券<p>' + data.start_time + '<br>' + data.end_time + '</p></div><i></i></div>');
    //     $item.appendTo($('.coupon'));
    // })
}

function already_use() {
    $('.coupon').empty();
    var used_data = coupons.usedCouponList
    $.each(used_data, function (i, data) {
        var $item = $('<div class="stamp stamp03"><div class="par"> <sub class="sign">' + "￥" + '</sub><span>' + data.face_value + '</span><p>优惠券</p><p>订单满' + data.lump_sum +
            '元</p> </div><div class="copy">副券<p>' + data.start_time + '<br>' + data.end_time + '</p></div><i></i></div>');
        $item.appendTo($('.coupon'));
    })
    // $.each(couponData.data2, function (i, data) {
    //     var $item = $('<div class="stamp stamp03"><div class="par"><span>' + data.face_value + '</span></div><div class="copy">副券<p>' + data.start_time + '<br>' + data.end_time + '</p></div><i></i></div>');
    //     $item.appendTo($('.coupon'));
    // })

}

function expire(){
    $('.coupon').empty();
    var expired_data = coupons.expiredCouponList;
    $.each(expired_data, function (i, data) {
        var $item = $('<div class="stamp stamp02"><div class="par"> <sub class="sign">' + "￥" + '</sub><span>' + data.face_value + '</span><p>优惠券</p><p>订单满' + data.lump_sum +
            '元</p> </div><div class="copy">副券<p>' + data.start_time + '<br>' + data.end_time + '</p></div><i></i></div>');
        $item.appendTo($('.coupon'));
    })
    // $.each(expired_data.data2, function (i, data) {
    //     var $item = $('<div class="stamp stamp02"><div class="par"><span>' + data.face_value + '</span></div><div class="copy">副券<p>' + data.start_time + '<br>' + data.end_time + '</p></div><i></i></div>');
    //     $item.appendTo($('.coupon'));
    // })
}


        