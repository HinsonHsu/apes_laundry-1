$(document).ready(function () {
    getData();

})
function getData() {
    $.ajax({
        type: "GET",
        url: "/products/products_all/",
        dataType: 'json',
        success: function (res) {
            console.log("receive:" + res.result);
            if (res.code == 1) {
                responseData = res

                loadData()
            } else {
                alert(res.errMsg)
            }
        },
        // error: onError
    })
}
function loadData() {
    console.log("loading")
    $('#categories').empty();
    $.each(responseData.data, function (i, data) {
        console.log("data:" + data.id)
        var $item = $('<div class="col-xs-6"><div class="thumbnail category-item"><a href="' + '/products/category/?id=' + data.id + '"><img src="' + "http://oyf9q4qzp.bkt.clouddn.com/" + data.logo +
            '"></a><div class="caption"><h4>' + data.name + '</h4></div></div></div>');
        $item.appendTo($('#categories'));

    })
    console.log("end")
}
var responseData = {
    data: [
        {
            "id": "1",
            "name": "大衣",
            "label": "overcoat",
            "pic": "images/大衣1.jpg"
        },
        {
            "id": "2",
            "name": "短袖",
            "label": "cotta",
            "pic": "images/短袖1.jpg"
        },
        {
            "id": "3",
            "name": "裤子",
            "label": "trousers",
            "pic": "images/裤子1.jpg"
        }
        ,
        {
            "id": "4",
            "name": "运动鞋",
            "label": "shoes",
            "pic": "images/运动鞋1.jpg"
        }
    ]
}
var responseData_overcoat = {
    data: [{
        "id": "11",
        "name": "大衣1",
        "pic": "images/大衣1.jpg"
    },
        {
            "id": "12",
            "name": "大衣2",
            "pic": "images/大衣2.jpg"
        },
        {
            "id": "13",
            "name": "大衣3",
            "pic": "images/大衣2.jpg"
        }
    ]
}
var responseData_cotta = {
    data: [{
        "id": "21",
        "name": "短袖1",
        "pic": "images/短袖1.jpg"
    }, {
        "id": "22",
        "name": "短袖2",
        "pic": "images/短袖2.jpg"
    }, {
        "id": "23",
        "name": "短袖3",
        "pic": "images/短袖3.jpg"
    }
    ]
}
var responseData_trousers = {
    data: [{
        "id": "31",
        "name": "裤子1",
        "pic": "images/裤子1.jpg"
    }, {
        "id": "32",
        "name": "裤子2",
        "pic": "images/裤子2.jpg"
    }, {
        "id": "33",
        "name": "裤子3",
        "pic": "images/裤子3.jpg"
    }

    ]
}
var responseData_shoes = {
    data: [{
        "id": "41",
        "name": "运动鞋1",
        "pic": "images/运动鞋1.jpg"
    }, {
        "id": "42",
        "name": "运动鞋2",
        "pic": "images/运动鞋2.jpg"
    }, {
        "id": "43",
        "name": "运动鞋3",
        "pic": "images/运动鞋3.jpg"
    }

    ]
}