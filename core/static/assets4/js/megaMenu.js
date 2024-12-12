$(document).ready(function () {

    $(".showSubMenu").click(function () {
        $(this).nextAll("ul").toggleClass("show");
        $(this).toggleClass('open');
    })

    let mainMenuHead = jQuery('.main-menu-head');

    $(mainMenuHead).hover(function () {
        $(this).children().find(".main-menu-sub").first().addClass('main-menu-sub-active');
        $(this).children().addClass('active');
    })

    $(mainMenuHead).mouseleave(function () {
        $(this).children().find(".main-menu-sub").first().removeClass('main-menu-sub-active');
        $(this).children().removeClass('active');
    })

    $(".main-menu li").mouseover(function () {

        $(".main-menu li").removeClass("main-menu-sub-active-li");
        $(this).addClass("main-menu-sub-active-li");
        $(".main-menu-sub").removeClass('main-menu-sub-active');
        $(this).children('ul').removeClass('main-menu-sub-active');
        $(this).children('ul').addClass('main-menu-sub-active');
    });

    $(".main-menu-sub-active").mouseleave(function () {
        $(".main-menu-sub-active").removeClass("main-menu-sub-active");
    })

})

/**
 * sticky mega menu
 * @type {Element}
 */

const megaMenu = document.querySelector(".mega");

window.addEventListener('scroll', function () {
    let windowScroll = window.pageYOffset;
    if (windowScroll >= 100){
        megaMenu.classList.add('active')
    } else{
        megaMenu.classList.remove('active')
    }
})
