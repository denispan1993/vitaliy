/**
 * Created by user on 26.01.14.
 */
try{jQuery(document).ready(function() {
        $('.auth-panel').tabSlideOut({
            tabHandle: '.auth-tab',                      //class of the element that will be your tab -doesnt have to be an anchor
            pathToTabImage:'/media/img/feedback_top_tab.gif', //relative path to the image for the tab
            imageHeight:'32px',                          //height of tab image
            imageWidth:'167px',                          //width of tab image
            tabLocation:'top',                           //side of screen where tab lives, top, right, bottom, or left
            speed:900,                                   //speed of animation
            action:'click',                              //options: 'click' or 'hover', action to trigger animation
            // topPos:'50px',                               //position from the top/ use if tabLocation is left or right
            // leftPos:'500px',                             //position from left/ use if tabLocation is bottom or top
            fixedPosition:true                           //options: true makes it stick(fixed position) on scroll
        });
    })
}catch(e){ alert(e) }
