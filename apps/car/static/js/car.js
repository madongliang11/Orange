$(function () {
    //点击’+‘实现商品数量递增效果
    $('.add').click(function () {
        //获取商品数量最大值
        let max_num = $(this).next().attr('max');
        //获取商品数量
        let num = $(this).next().val();
        // 商品单价
        let single_price = $(this).parent().parent().prev().text();
        if (parseInt(num) < parseInt(max_num)){
            num ++ ;
            $(this).next().val(num);
            let $check_box = $(this).parent().parent().prevAll('li').find('input');
            if ($check_box.is(':checked')) {
                var all_price = $('#total>em').text();
                var total_shop = $('#total>b').text();
                all_price = all_price*1 + single_price*1;
                $('#total>em').text(all_price);
                total_shop = total_shop*1 + 1;
                $('#total>b').text(total_shop)
            }
        }else {
            $(this).next().val(num);
        }
        // 商品总价
        let total_price = toDecimal2(num * single_price);
        $(this).parent().parent().next().text(total_price);
        let shop_id = $(this).prev().prop('add_shop_id')
    });
    //点击’-‘实现商品数量递减效果
    $('.minus').click(function () {
        //获取商品数量
        let num = $(this).prev().val();
        // 商品单价
        let single_price = $(this).parent().parent().prev().text();
        if (num > 1){
            num -- ;
            $(this).prev().val(num);
            let $check_box = $(this).parent().parent().prevAll('li').find('input');
            if ($check_box.is(':checked')) {
                var all_price = $('#total>em').text();
                var total_shop = $('#total>b').text();
                all_price = all_price*1 - single_price*1;
                $('#total>em').text(all_price)
                total_shop = total_shop*1 - 1;
                $('#total>b').text(total_shop)

            }
        }else {
            $(this).prev().val(num);
        }
        // 商品总价
        let total_price = toDecimal2(num * single_price);
        $(this).parent().parent().next().text(total_price);
    });

    // {#其他类型转化带两位小数的float#}
            function toDecimal2(x) {
            var f = parseFloat(x);
            if (isNaN(f)) {
                return false;
            }
            var f = Math.round(x * 100) / 100;
            var s = f.toString();
            var rs = s.indexOf('.');
            if (rs < 0) {
                rs = s.length;
                s += '.';
            }
            while (s.length <= rs + 2) {
                s += '0';
            }
            return s;
        }

});

// 全选，全不选
$(function () {
    $('#all_check').click(function () {
        if ($(this).prop('checked')){
            $('input[name="checkbox"]').each(function (index,ele) {
                $(ele).prop('checked',true);
                let shop_num = $(this).parent().nextAll('.col06').find('input').val();
                let price = $(this).parent().nextAll('.col07').text();
                var all_price = $('#total>em').text();
                var total_shop = $('#total>b').text();
                all_price = all_price*1 + price*1;
                total_shop = total_shop*1 + shop_num*1;
                $('#total>em').text(all_price);
                $('#total>b').text(total_shop);
            });
        }else {
            $('input[name="checkbox"]').each(function (index,ele) {
                $(ele).prop('checked',false);
                let shop_num = $(this).parent().nextAll('.col06').find('input').val();
                let price = $(this).parent().nextAll('.col07').text();
                var all_price = $('#total>em').text();
                var total_shop = $('#total>b').text();
                all_price = all_price*1 - price*1;
                total_shop = total_shop*1 - shop_num*1;
                $('#total>em').text(all_price);
                $('#total>b').text(total_shop);
            });
        }

    });


    // {#给每一个checkbox添加点击效果#}
    let $sonCheckBox = $('.son_check');
    $sonCheckBox.each(function () {
        $(this).click(function () {
            if ($(this).is(':checked')) {
                let shop_num = $(this).parent().nextAll('.col06').find('input').val();
                let price = $(this).parent().nextAll('.col07').text();
                var all_price = $('#total>em').text();
                var total_shop = $('#total>b').text();
                all_price = all_price*1 + price*1;
                total_shop = total_shop*1 + shop_num*1;
                $('#total>em').text(all_price);
                $('#total>b').text(total_shop);
        //判断：所有单个商品是否勾选
                var len = $sonCheckBox.length;
                var num = 0;
                $sonCheckBox.each(function () {
                    if ($(this).is(':checked')) {
                        num++;
                    }
                });
                if (num === len) {
                    $('#all_check').prop("checked", true);

                }
            } else {
        //单个商品取消勾选，全局全选取消勾选
                $('#all_check').prop("checked", false);
                let shop_num = $(this).parent().nextAll('.col06').find('input').val();
                let price = $(this).parent().nextAll('.col07').text();
                var all_price = $('#total>em').text();
                var total_shop = $('#total>b').text();
                all_price = all_price*1 - price*1;
                total_shop = total_shop*1 - shop_num*1;
                $('#total>em').text(all_price);
                $('#total>b').text(total_shop)

            }
        })
    })
});
