$(document).ready(function() {
        $("li").hover(function() {
            $(".category-content .category-list li.first .menu-in").css("display", "none");
            $(".category-content .category-list li.first").removeClass("hover");
            $(this).addClass("hover");
            $(this).children("div.menu-in").css("display", "block")
        }, function() {
            $(this).removeClass("hover")
            $(this).children("div.menu-in").css("display", "none")
        });
    })