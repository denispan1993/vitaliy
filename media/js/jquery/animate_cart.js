/**
 * Created with PyCharm.
 * User: Sergey
 * Date: 18.07.13
 * Time: 19:07
 * To change this template use File | Settings | File Templates.
 */
var Cart = new Object({initialize: function(){},toggle: function(){$('#cart').toggleClass('opened');}});

/*function open_cart(obj){
    $(obj).toggleClass('opened');
};*/

function animate_cart(obj){
    src = obj.src;
    left_cart = Math.ceil($(obj).offset().left);
    top_cart = Math.ceil($(obj).offset().top);
    $('<img src="'+src+'" id="temp_cart_animate" style="z-index:1000;position:absolute;top:'+top_cart+'px;left:'+left_cart+'px;">').prependTo('body');
    //$('#cart').addClass('opened');
    $('#temp_cart_animate').animate({top: 220+$(window).scrollTop(), left: $('body').width()}, 2000,
        function () {
            //$('#cart').removeClass('opened');
            $('#temp_cart_animate').remove();
        }
    );
}