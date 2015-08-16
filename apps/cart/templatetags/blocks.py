# coding=utf-8
__author__ = 'Sergey'

from django_jinja.library import Library
from django.template.loader import render_to_string

register = Library()


@register.global_function()
def block_cart(request, cart, coupon, place_of_use='cart', ):
    # request_csrf_token = request.META.get(u"CSRF_COOKIE", None, )
    # request_csrf_token = request.COOKIES.get(u'csrftoken', None, )
    request_csrf_token = None
    template_name = u'templatetags/block_cart.jinja2.html'
    form1_action = None
    form2_action = None
    if place_of_use == 'cart':
        form1_action = u'/корзина/пересчитать/'
        # if request.user.is_authenticated and request.user.is_staff:
        form2_action = u'/заказ/первый-шаг/'
        # else:
        #     form2_action = u'/корзина/заказ/'
        from django.middleware.csrf import get_token
        request_csrf_token = get_token(request, )
    elif place_of_use == 'order':
        template_name = u'templatetags/block_order.jinja2.html'

    return render_to_string(template_name,
                            dictionary={'request': request,
                                        'cart': cart,
                                        'coupon': coupon,
                                        'place_of_use': place_of_use,
                                        'form1_action': form1_action,
                                        'form2_action': form2_action,
                                        'csrf_token': request_csrf_token, }, )
#