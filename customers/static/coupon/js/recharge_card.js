$(document).ready(function () {

})
var radioIndex = -1;
var real_money = -1;
var fake_money = 0;
function moneyChanged(val) {
    var s = parseFloat(val);
    real_money = s;
    if (radioIndex >= 0 && customer_card_charge_setting[radioIndex].min <= s) {
        s = s + customer_card_charge_setting[radioIndex].money_give;
    }
    s = parseFloat(s).toFixed(1);
    $("#money_obtain").text(s)
}
function onRadioClick(val) {

    radioIndex = val;
    if (real_money > 0 && customer_card_charge_setting[radioIndex].min <= real_money) {
        fake_money = real_money + customer_card_charge_setting[radioIndex].money_give;
        fake_money = parseFloat(fake_money).toFixed(1);
        $("#money_obtain").text(fake_money)
    }

}
function onCharge() {
    minusMoney = 0;
    if (radioIndex >= 0 && customer_card_charge_setting[radioIndex].min <= real_money) {
        minusMoney = customer_card_charge_setting[radioIndex].money_give;
    } else {
        minusMoney = 0
    }
    $.ajax({
        type: "POST",
        url: "/customer/recharge/",
        data: {'real_money': real_money, 'fake_money': minusMoney},
        dataType: 'json',
        success: function (data) {
            // $("#checkCode").val(data.code)
            console.log("receive:" + data.code);
            if (data.code == 0) {
                alert('充值成功!')
            } else {
                alert('充值失败')
            }

        },
        // error: onError
    });
}