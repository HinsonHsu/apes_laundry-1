/**
 * Created by H1nson on 2017/11/5.
 */
var category_data = [];
var cart_data = []
var totalPrice = 0
$(document).ready(function () {
    city_id = sessionStorage.getItem("city_id")
    $("#address-select").val(city_id)
    calculateTotalPrice()
    getData(city_id);
})
function calculateTotalPrice() {
    cart_data = JSON.parse(localStorage.getItem("cart_data"));
    if (cart_data != null) {
        for (var i = 0; i < cart_data.length; i++) {
            totalPrice += cart_data[i].amount * cart_data[i].price
        }
    }

    $("#total-price").text(totalPrice)
}
function changeAdd(city_id) {
    sessionStorage.setItem("city_id", city_id)
    getData(city_id)
}
function getData(city_id) {
    var category_id = getUrlParam('id');
    console.log("categoryid:" + category_id + "city_id:" + city_id)
    $.ajax({
        type: "GET",
        url: "/products/products_by_category/",
        dataType: 'json',
        data: {category_id: category_id, city_id: city_id},
        success: function (res) {
            console.log("receive:" + res.result);
            console.log("receive:" + res.category);
            if (res.code == 1) {
                $("#title").text(res.category)
                loadData(res)
            } else {
                alert(res.errMsg)
            }
        },
        // error: onError
    })
}
function loadData(responseData) {
    category_data = responseData.data
    $('#categories').empty();
    $.each(responseData.data, function (i, data) {
        var $item = $('<div class="col-xs-6" onclick="add_to_cart(' + i + ')"><div class="thumbnail category-item"><img src="' + "http://oyf9q4qzp.bkt.clouddn.com/" + data.logo +
            '"><div class="caption"><h4>' + data.name + '</h4></div>' + '<div class="price"><h5>' + data.price + '</h5></div>' + '</div></div>');
        $item.appendTo($('#categories'));
    })
}
//获取url中的参数
function getUrlParam(name) {
    var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)"); //构造一个含有目标参数的正则表达式对象
    var r = window.location.search.substr(1).match(reg);  //匹配目标参数
    if (r != null) return unescape(r[2]);
    return null; //返回参数值
}

function add_to_cart(index) {
    var flag = true
    if(cart_data == null){
        cart_data = []
    }
    for (var i = 0; i < cart_data.length; i++) {
        if (cart_data[i].id == category_data[index].id) {
            cart_data[i].amount = cart_data[i].amount + 1
            flag = false
            totalPrice += cart_data[i].price
        }
    }
    if (flag) {
        i = category_data[index]
        var newObject = jQuery.extend(true, {}, i);
        newObject.amount = 1
        cart_data.push(newObject)
        totalPrice += newObject.price
    }
    $("#total-price").text(totalPrice)
    obj = JSON.stringify(cart_data); //转化为JSON字符串
    localStorage.setItem("cart_data", obj);//返回{"a":1,"b":2}
}