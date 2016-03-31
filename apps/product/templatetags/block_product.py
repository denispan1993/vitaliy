# -*- coding: utf-8 -*-
from django_jinja.library import Library
from django.template.loader import render_to_string

__author__ = 'AlexStarov'

register = Library()


@register.global_function()
def block_products(products, request, ):
    from django.middleware.csrf import get_token
    request_csrf_token = get_token(request, )
    # request_csrf_token = request.META.get(u"CSRF_COOKIE", None, )
    # request_csrf_token = request.COOKIES.get(u'csrftoken', None, )
    # from proj.settings import MEDIA_URL
    return render_to_string(template_name=u'product/templatetags/block_products.jinja2.html',
                            dictionary={'products': products,
                                        'request': request,
                                        'csrf_token': request_csrf_token, }, )


@register.global_function()
def block_product(product, choice, cycle, last_loop, ):
    if last_loop:
        margin_bottom = '0px'
    else:
        margin_bottom = '10px'
    if cycle == 1:
        margin_left = '0px'
    else:
        margin_left = '10px'
    return render_to_string(template_name=u'product/templatetags/block_product.jinja2.html',
                            dictionary={'product': product,
                                        'choice': choice,
                                        'margin_bottom': margin_bottom,
                                        'margin_left': margin_left, }, )
