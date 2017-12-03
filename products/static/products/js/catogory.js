/**
 * Created by H1nson on 2017/11/5.
 */
$(document).ready(function () {
    getData(3);

})
function changeAdd(city_id) {
    getData(city_id)
}
function getData(city_id) {
    var category_id = getUrlParam('id');
    console.log("categoryid:" + category_id + "city_id:"+city_id)
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
    $('#categories').empty();
    $.each(responseData.data, function (i, data) {
        var $item = $('<div class="col-xs-6"><div class="thumbnail category-item"><img src="' + "http://oyf9q4qzp.bkt.clouddn.com/" + data.logo +
            '"><div class="caption"><h4>' + data.name + '</h4></div>'+'<div class="price"><h5>'+data.price+'</h5></div>'+'</div></div>');
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