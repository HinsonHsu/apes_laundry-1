(function($) {
    $.alerts = {
        confirm: function(title, message, callback) {
            if( title == null ) title = 'Confirm';
            $.alerts._show(title, message, null, 'confirm', function(result) {
                if( callback ) callback(result);
            });
        },
        _show: function(title, msg, value, type, callback) {
            var _html = "";
            _html += '<div id="mb_box"></div><div id="mb_con">'+ '<div id="mb_msg">' + msg + '</div><div id="mb_btnbox">'+ '<input id="mb_btn_ok" type="button" value="确定" />'+'<input id="mb_btn_no" type="button" value="取消" />'+'</div></div>';
            //必须先将_html添加到body，再设置Css样式
            $("body").append(_html); GenerateCss();

            switch( type ) {
                case 'confirm':

                    $("#mb_btn_ok").click( function() {
                        $.alerts._hide();
                        if( callback ) callback(true);
                    });
                    $("#mb_btn_no").click( function() {
                        $.alerts._hide();
                        if( callback ) callback(false);
                    });
                    $("#mb_btn_no").focus();
                    $("#mb_btn_ok, #mb_btn_no").keypress( function(e) {
                        if( e.keyCode == 13 ) $("#mb_btn_ok").trigger('click');
                        if( e.keyCode == 27 ) $("#mb_btn_no").trigger('click');
                    });
                    break;
            }
        },
        _hide: function() {
            $("#mb_box,#mb_con").remove();
        }
    }
    zdconfirm = function(title, message, callback) {
        $.alerts.confirm(title, message, callback);
    };
    //生成Css
    var GenerateCss = function () {
        var _widht = document.documentElement.clientWidth; //屏幕宽
        var _height = document.documentElement.clientHeight; //屏幕高
        var boxWidth = $("#mb_con").width();
        var boxHeight = $("#mb_con").height();
        //让提示框居中
        $("#mb_con").css({ top: (_height - boxHeight) / 2 + "px", left: (_widht - boxWidth) / 2 + "px" });
    }
})(jQuery);
