# coding=utf-8
__author__ = 'Sergey'

from django_jinja.library import Library
from django.template.loader import render_to_string

register = Library()


@register.global_function()
def block_products(products, request, ):
    from django.middleware.csrf import get_token
    request_csrf_token = get_token(request, )
    # request_csrf_token = request.META.get(u"CSRF_COOKIE", None, )
    # request_csrf_token = request.COOKIES.get(u'csrftoken', None, )
    return render_to_string(template_name=u'product/templatetags/block_products.jinja2.html',
                            dictionary={'products': products,
                                        'request': request,
                                        'csrf_token': request_csrf_token, }, )


@register.global_function()
def block_product(product, choice, cycle, ):
    if cycle == 1:
        product_block = 'first_product_block'
    else:
        product_block = 'product_block'
    return render_to_string(template_name=u'product/templatetags/block_product.jinja2.html',
                            dictionary={'product': product,
                                        'choice': choice,
                                        'product_block': product_block, }, )
