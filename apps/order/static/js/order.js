$(function () {
    let $first_addr = $('#first_addr');
    let $holyshit268 = $('#holyshit268');
    let $holyshit269 = $('#holyshit269');
    let aid = $first_addr.attr('aid');
    $holyshit269.attr('aid',aid);
    let province = $first_addr.find('.province').text();
    let city = $first_addr.find('.city').text();
    let dist = $first_addr.find('.dist').text();
    let street = $first_addr.find('.street').text();
    let username = $first_addr.find('.buy-user').text();
    let phone = $first_addr.find('.buy-phone').text();
    $holyshit268.find('.province').text(province);
    $holyshit268.find('.city').text(city);
    $holyshit268.find('.dist').text(dist);
    $holyshit268.find('.street').text(street);
    $holyshit268.find('.buy-user').text(username);
    $holyshit268.find('.buy-phone').text(phone);
});

$(function() {
    $(".user-addresslist").click(function() {
        $(this).addClass("defaultAddr").siblings().removeClass("defaultAddr");
        let $defaultAddr = $('.defaultAddr');
        let $holyshit268 = $('#holyshit268');
        let $holyshit269 = $('#holyshit269');
        let aid = $defaultAddr.attr('aid');
        $holyshit269.attr('aid',aid);
        let province = $defaultAddr.find('.province').text();
        let city = $defaultAddr.find('.city').text();
        let dist = $defaultAddr.find('.dist').text();
        let street = $defaultAddr.find('.street').text();
        let username = $defaultAddr.find('.buy-user').text();
        let phone = $defaultAddr.find('.buy-phone').text();
        $holyshit268.find('.province').text(province);
        $holyshit268.find('.city').text(city);
        $holyshit268.find('.dist').text(dist);
        $holyshit268.find('.street').text(street);
        $holyshit268.find('.buy-user').text(username);
        $holyshit268.find('.buy-phone').text(phone);
    });
    $(".logistics").each(function() {
        var i = $(this);
        var p = i.find("ul>li");
        p.click(function() {
            if (!!$(this).hasClass("selected")) {
                $(this).removeClass("selected");
            } else {
                $(this).addClass("selected").siblings("li").removeClass("selected");
            }
        })
    })
});

// 弹出地址选择

$(document).ready(function($) {

    var $ww = $(window).width();

    $('.theme-login').click(function() {
//					禁止遮罩层下面的内容滚动
        $(document.body).css("overflow","hidden");

        $(this).addClass("selected");
        $(this).parent().addClass("selected");


        $('.theme-popover-mask').show();
        $('.theme-popover-mask').height($(window).height());
        $('.theme-popover').slideDown(200);

    })

    $('.theme-poptit .close,.btn-op .close').click(function() {

        $(document.body).css("overflow","visible");
        $('.theme-login').removeClass("selected");
        $('.item-props-can').removeClass("selected");
        $('.theme-popover-mask').hide();
        $('.theme-popover').slideUp(200);
    })
});


//点击提交订单
$(function () {
    $('#J_Go').click(function () {
        var aid = $('#holyshit269').attr('aid');
        var total = $('#J_ActualFee').text();
        //获取当前网页url跟在问号后面的部分。？oid=1&k=8
        var oid = window.location.search;
        var num = oid.indexOf("=");
        var id = oid.substring(num+1);
        window.location.href = '/pay/pay/?oid=' + id + '&total='+total+'&aid='+aid
    })
});


