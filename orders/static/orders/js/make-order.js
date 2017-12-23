/**
 * Created by H1nson on 2017/12/10.
 */
var cart_data = []
var totalPrice = 0
$(document).ready(function () {
    calculateTotalPrice()
})
function calculateTotalPrice() {
    cart_data = JSON.parse(localStorage.getItem("cart_data"));
    for (var i = 0; i < cart_data.length; i++) {
        totalPrice += cart_data[i].amount * cart_data[i].price
        var $item = $('<div class="order-item"> <div class="item-name">'+cart_data[i].name+'</div><div class="item-price">￥'+cart_data[i].price+'</div><div class="item-amount">数量 * '+cart_data[i].amount+'</div></div>')
        $item.appendTo($("#order-items"))
    }
    $("#total-price").text(totalPrice)
}
function make_order() {
    $("#cart-right").attr("disabled", true);
    city_id = sessionStorage.getItem("city_id")
    cart_data.push({"city_id": city_id})
    $.ajax({
        type: "POST",
        url: "/orders/make_order/",
        data: JSON.stringify(cart_data),
        dataType: 'json',
        success: function (res) {
            console.log("receive:" + res);
            if (res.code == 1) {
                alert("下单成功")
                localStorage.removeItem('cart_data');
                window.location.href = "/products/index/"
            } else {
                alert("下单失败")
                alert(res.errMsg)
            }
        },
        // error: onError
    })
}