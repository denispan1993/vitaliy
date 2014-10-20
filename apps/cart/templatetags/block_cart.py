# coding=utf-8
__author__ = 'Sergey'

from django_jinja.library import Library
from django.template.loader import render_to_string

register = Library()


@register.global_function()
def block_cart(request, cart, place_of_use='cart', ):
    # request_csrf_token = request.META.get(u"CSRF_COOKIE", None, )
    # request_csrf_token = request.COOKIES.get(u'csrftoken', None, )
    request_csrf_token = None
    template_name = u'templatetags/block_cart.jinja2.html'
    form1_action = u'/корзина/пересчитать/'
    form2_action = u'/корзина/заказ/'
    if place_of_use == 'cart':
        from django.middleware.csrf import get_token
        request_csrf_token = get_token(request, )

    return render_to_string(template_name,
                            dictionary={'request': request,
                                        'cart': cart,
                                        'place_of_use': place_of_use,
                                        'form1_action': form1_action,
                                        'form2_action': form2_action,
                                        'csrf_token': request_csrf_token, }, )
