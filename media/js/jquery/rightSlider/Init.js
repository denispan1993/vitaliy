/**
 * Created by user on 18.01.14.
 */
try{
    $(document).ready(function($){
        $('.rightSlider').bxSlider({
            mode:'vertical',
            slideWidth:300,
            minSlides:3,
            slideMargin:10,
            moveSlides:1,
            auto:true,
            autoControls:true,
            pause:4000,
            autoHover:true,
            autoDelay:2000
//            slideMargin:5
        });
    });
}catch(e){ alert(e) }
