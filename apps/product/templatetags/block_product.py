# coding=utf-8
__author__ = 'Sergey'

from django_jinja.library import Library
from django.template.loader import render_to_string

register = Library()


@register.global_function()
def block_products(products, ):
    return render_to_string(template_name=u'product/templatetags/block_products.jinja2.html',
                            dictionary={'products': products, }, )


@register.global_function()
def block_product(product, ):
    return render_to_string(template_name=u'product/templatetags/block_product.jinja2.html',
                            dictionary={'product': product, }, )

