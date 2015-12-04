/**
 * Created by user on 26.01.14.
 */
try{jQuery(document).ready(function() {
        $('.feedback-panel').tabSlideOut({
            tabHandle:'.feedback-tab',                   //class of the element that will be your tab -doesnt have to be an anchor
            pathToTabImage:'/media/img/feedbacktab-ru.jpeg', //relative path to the image for the tab
            imageHeight:'150px',                          //height of tab image
            imageWidth:'30px',                           //width of tab image
            tabLocation:'left',                          //side of screen where tab lives, top, right, bottom, or left
            speed:500,                                   //speed of animation
            action:'click',                              //options: 'click' or 'hover', action to trigger animation
            topPos:'50px',                               //position from the top/ use if tabLocation is left or right
            // leftPos:'20px',                              //position from left/ use if tabLocation is bottom or top
            fixedPosition:false                          //options: true makes it stick(fixed position) on scroll
        });
    })
}catch(e){ alert(e) }
