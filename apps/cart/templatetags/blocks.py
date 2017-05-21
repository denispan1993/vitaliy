# -*- coding: utf-8 -*-

from django_jinja.library import global_function
from django.template.loader import render_to_string
from django.middleware.csrf import get_token

__author__ = 'AlexStarov'


@global_function()
def block(request, cart=None, order=None, place_of_use='cart', ):
    context = {'request': request,
               'place_of_use': place_of_use, }
    if place_of_use == 'cart':
        form1_action = u'/корзина/пересчитать/'
        form2_action = u'/заказ/первый-шаг/'

        request_csrf_token = get_token(request, )

        context.update({'cart': cart,
                        'form1_action': form1_action,
                        'form2_action': form2_action,
                        'csrf_token': request_csrf_token, })

        return render_to_string(template_name='templatetags/block_cart.jinja2',
                                context=context, )

    elif place_of_use == 'order':

        context.update({'order': order, })

        return render_to_string(template_name='templatetags/block_order.jinja2',
                                context=context, )

# request_csrf_token = request.META.get(u"CSRF_COOKIE", None, )
# request_csrf_token = request.COOKIES.get(u'csrftoken', None, )
