# coding=utf-8
__author__ = 'Sergey'

from django_jinja.library import Library
from django.template.loader import render_to_string

register = Library()


@register.global_function()
def block_products_div(products, request, ):
    from django.middleware.csrf import get_token
    request_csrf_token = get_token(request, )
    # request_csrf_token = request.META.get(u"CSRF_COOKIE", None, )
    # request_csrf_token = request.COOKIES.get(u'csrftoken', None, )
    return render_to_string(template_name=u'product/templatetags/block_products-div.jinja2.html',
                            dictionary={'products': products, 'csrf_token': request_csrf_token, }, )


@register.global_function()
def block_products_li(products, request, ):
    from django.middleware.csrf import get_token
    request_csrf_token = get_token(request, )
    # request_csrf_token = request.META.get(u"CSRF_COOKIE", None, )
    # request_csrf_token = request.COOKIES.get(u'csrftoken', None, )
    return render_to_string(template_name=u'product/templatetags/block_products-li.jinja2.html',
                            dictionary={'products': products, 'csrf_token': request_csrf_token, }, )


@register.global_function()
def block_product(product, ):
    return render_to_string(template_name=u'product/templatetags/block_product.jinja2.html',
                            dictionary={'product': product, }, )

