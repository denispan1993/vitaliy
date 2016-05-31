/**
 * Created by user on 18.01.14.
 */
try{
$(function($){
    $('.rightSlider').bxSlider({
        mode:'vertical',
        slideWidth:300,
        minSlides:3,
        maxSlides:3,
        slideMargin:10,
        moveSlides:1,
        auto:true,
        autoStart:true,
        controls:false,
        autoControls:false,
        pager:true,
        pagetType:'short',
        pause:5000,
        autoHover:true,
        autoDelay:5000
//            slideMargin:5
    });
});
}catch(e){console.log(e);}
