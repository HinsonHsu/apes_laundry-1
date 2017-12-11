$(function () {

    $(".icon").addClass("icon-selected");  //初始全选
    // 总价
    function totalPrices() {
        var Totalprices = 0;  //总价
        var pricelen = 0;     //商品数量
        $("div.order-select .icon.icon-selected").each(function () {
            var $_this = $(this);

            var len = $_this.length;

            var price = Number($_this.parents(".grid-order").find(".ui-price-iconleft").text());

            Totalprices += price;
            pricelen += len;
        });
        if (pricelen == 0) {
            $("button.go-btn").attr("disabled", true)
        } else {
            $("button.go-btn").attr("disabled", false)
        }
        $("span.total_prices").text(pricelen);
        $("span.total-fee").text(Totalprices.toFixed(2));
    }

    totalPrices();


    //判断当前“减”按钮是否可用
    $("span.ui-number").each(function () {
        if ($(this).children("input").val() == "1") {
            $(this).children("a:first-child").addClass("disabled");
        }
    });

    //减
    $("a.decrease ").on("click", function () {
        var $num = $(this).next("input");
        if (parseInt($num.val()) > 1) {
            $num.val(parseInt($num.val()) - 1);
            numProdcut($(this), $num.val());
            totalPrices();
            var $p = $(this).parent()
            var $p = $p.parent()
            var $p = $p.parent()
            var index = $p.index()
            cart_data[index].amount -= 1
            obj = JSON.stringify(cart_data); //转化为JSON字符串
            localStorage.setItem("cart_data", obj)
        }
        if (parseInt($num.val()) == 1) {
            $(this).addClass("disabled");
            return false;
        }

    });
    //加
    $("a.increase").on("click", function () {
        var $num = $(this).prev("input");

        $num.val(parseInt($num.val()) + 1);
        var $p = $(this).parent()
        var $p = $p.parent()
        var $p = $p.parent()
        var index = $p.index()
        cart_data[index].amount += 1
        obj = JSON.stringify(cart_data); //转化为JSON字符串
        localStorage.setItem("cart_data", obj)
        if ($num.val() > 1) {
            $(this).siblings("a.decrease").removeClass("disabled");
        }
        numProdcut($(this), $num.val());
        totalPrices();

    });

    $(".order-select").click(function () {
//            var len=$(".grid-main").children().length;
        if ($(this).hasClass("shop-select")) {
            if ($(this).children("div").hasClass("icon-selected")) {

                $(this).children("div").removeClass("icon-selected");
                $(".icon").removeClass("icon-selected");
                $(".total-right p:first-child").addClass("hide");
                $(".total-right p:last-child").removeClass("hide");
                totalPrices();
            } else {
                $(".icon").addClass("icon-selected");
                $(this).children("div").addClass("icon-selected");
                $(".total-right p:first-child").removeClass("hide");
                $(".total-right p:last-child").addClass("hide");
                totalPrices();
            }
        }
        else if ($(this).children("div").hasClass("icon-selected")) {
            $(this).children("div").removeClass("icon-selected");
            $("a.shop-select").children("div").removeClass("icon-selected");
            $(".total-right p:first-child").addClass("hide");
            $(".total-right p:last-child").removeClass("hide");
            totalPrices();
        }
        else if (!$(this).children("div").hasClass("icon-selected")) {
            $(this).children("div").addClass("icon-selected");
            checkAll();
            totalPrices();
        }
    });

    // 点击清空按钮
    $("p.empty_product").on("click", function () {
        zdconfirm('', '你确定清空吗', function (r) {
            if (r) {
                $(" div.order-list").animate({"opacity": 0}, 400, function () {
                    $(" div.order-list").remove();
                    checkAll();
                    totalPrices();
                });
                localStorage.removeItem('cart_data');
            }
            else {
                return false;
            }
        });
    });

    //点击删除按钮
    $("p.clear_product").on("click", function () {
        if ($("div.icon.icon-selected").length == 0) {
            alert_mt();
        }
        else {
            zdconfirm('', '你确认删除数据吗', function (r) {
                if (r) {
                    var del = [];
                    $.each($(" div.icon-selected"), function () {
                        index = $(this).parents("div.grid-order").index()
                        del.push(cart_data[index].id)
                    })
                    for (var j = 0; j < del.length; j++) {
                        for (var i = 0; i < cart_data.length; i++) {
                            if (cart_data[i].id == del.id) {
                                car_data.splice(i,i)
                            }
                        }

                    }

                    $(" div.icon-selected").parents("div.grid-order").animate({"opacity": 0}, 400, function () {
                        $(" div.icon-selected").parents("div.grid-order").remove();
                        checkAll();
                        totalPrices();
                    });

                }
                else {
                    return false;
                }
            });
        }

    });


    //点击单个 删除按钮
    $("a.opt-delete").on("click", function () {
        var $_this = $(this);
        zdconfirm('', '你确认删除数据吗', function (r) {
            if (r) {
                if ($(".grid-main div.icon-selected").length != 1) {
                    $_this.parents("div.grid-order").animate({"opacity": 0}, 400, function () {
                        $_this.parents("div.grid-order").remove();
                        checkAll();
                        totalPrices();
                    });
                }
                else {
                    $(" div.order-list").animate({"opacity": 0}, 400, function () {
                        $(" div.order-list").remove();
                        checkAll();
                        totalPrices();
                    });
                }
            }
            else {
                return false;
            }
        });
    });

    // 全选 点击删除后做全选
    function checkAll() {
        var len = $(".grid-main").children().length;
        var checklen = $(".grid-main div.icon-selected").length;
        if (len == checklen) {
            $("a.shop-select").children("div").addClass("icon-selected");
            $(".total-right p:first-child").removeClass("hide");
            $(".total-right p:last-child").addClass("hide");
        }
        if (len == 0) {
            var skip_home_page = "<div class='mui-prompt-empty'><ins></ins><span class='mui-prompt-icon'>" +
                "</span><ins></ins><div><p>购物车还是空的，</p><p>去挑几件中意的商品吧</p></div><a class='mui-prompt-btn' href='/products/index/'>开始购物</a></div>";
            $("#R_Main").empty().append(skip_home_page);


        }
    }

    //       单个数量的个数 级总价
    function numProdcut(_this, num) {
        var numA = _this.parents("div.order-des").next("div.order-opt").children("div.opt-num");
        numA.text(numA.text().split("x")[0] + "x" + num);
        var numprice = _this.siblings("input[type='hidden']").val();
        var numM = _this.parents("div.order-des").next("div.order-opt").find("span.ui-price-iconleft");
        numM.text(parseFloat(numprice * num).toFixed(2));
    }

    // 结算点击事件

    function Balance() {
        window.location.href = '/orders/make_order/';
    }

    $("button.go-btn").on("click", function () {
            Balance()

        }
    );

    function alert_mt() {
        var htm = '<div class="alert_mt"><span>您没有选中要删除的商品</span></div>';
        $("body").append(htm);
        $(".alert_mt").fadeIn(100);
        setTimeout(function () {
            $(".alert_mt").fadeOut(100, function () {
                $("div.alert_mt").remove()
            });
        }, 1000);
    }


});