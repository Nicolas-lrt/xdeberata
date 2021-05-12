jQuery(document).ready(function() {
    "use strict";    
    
    /*===================== TABLE OF CONTENT =======================
    1. Home Page Slider
    2. Search Icon
    3. Twitter Slider
    4. Responsive Menu
    4. Responsive Menu Dropdown
    4. Footer Instagram Slider
    4. Go to Top Button
    =============================================================*/
    
    /* Home Page Slider */
    $('.post-slider').owlCarousel({
        items:1,
        loop:true,
        autoHeight:true,
        autoplay:false,
        autoplayTimeout:5000,
        smartSpeed:1000,
        nav:true,
        navText:['<i class="fa fa-angle-left" aria-hidden="true"></i>','<i class="fa fa-angle-right" aria-hidden="true"></i>']
    });
    
    /* Search Icon */
    $(".search-icon i").on("click",function(){
        $(this).toggleClass("active");
        $(".search-box").toggleClass("searchon");
        return false;
    });
    
    /* Twitter Slider */
    $('.twitter-slider').owlCarousel({
        items:1,
        loop:true,
        autoHeight:true,
        autoplay:true,
        autoplayTimeout:6000,
        smartSpeed:1000,
        nav:false,
        dots:true
    });
    
    /* Responsive Menu */
    $(".menu-button, .stop").on("click",function(){
        $(this).toggleClass("active");
        $(".responsive-menu").toggleClass("slidein");
        $(".theme-layout").toggleClass("stop");
        return false;
    });
    
    /* Responsive Menu Dropdown */
    $(".mobile-menu ul").parent().addClass("menu-item-has-children");
    $(".mobile-menu li.menu-item-has-children > a").on("click",function(){
        $(this).next("ul").slideToggle();
        $(this).parent().siblings().find("ul").slideUp();
        return false;
    });
    
    /* Footer Instagram Slider */
    $('.insta-slider').owlCarousel({
        loop:true,
        items:4,
        nav:false,
        responsive : {

            480 : {
                items : 5
            },
            
            768 : {
                items : 6
            },
            
            1200 : {
                items : 7
            }
        }
    });
    
    /* Go Top Button */
    $("#up").on("click",function (){
        $('html, body').animate({
            scrollTop: $(".theme-layout").offset().top
        }, 1000);
    });
    
}); /*=== Document.Ready Ends Here ===*/
