# coding=utf-8
__author__ = 'Sergey'

from django_jinja.library import Library
from django.template.loader import render_to_string

register = Library()


@register.global_function()
def many_blocks(blocks, request, current_currency, category_or_product, top_border, ):
    # request_csrf_token = request.META.get(u"CSRF_COOKIE", None, )
    # request_csrf_token = request.COOKIES.get(u'csrftoken', None, )
    if category_or_product == 'category':
        template_name=u'category/templatetags/block_categories.jinja2.html'
        request_csrf_token = None
    elif category_or_product == 'product':
        from django.middleware.csrf import get_token
        request_csrf_token = get_token(request, )
        template_name=u'product/templatetags/block_products.jinja2.html'
    return render_to_string(template_name,
                            dictionary={'blocks': blocks,
                                        'request': request,
                                        'current_currency_': current_currency,
                                        'csrf_token': request_csrf_token,
                                        'top_border': top_border, }, )


@register.global_function()
def one_block(block, request, current_currency, choice, cycle, last_loop, category_or_product, ):
    print(last_loop)
    if last_loop:
        margin_bottom = '0px'
    else:
        margin_bottom = '10px'
    if cycle == 1:
        margin_left = '0px'
    else:
        margin_left = '10px'
    if category_or_product == 'category':
        template_name = u'category/templatetags/block_category.jinja2.html'
    elif category_or_product == 'product':
        template_name = u'product/templatetags/block_product.jinja2.html'
    return render_to_string(template_name,
                            dictionary={'block': block,
                                        'request': request,
                                        'current_currency_': current_currency,
                                        'choice': choice,
                                        'margin_bottom': margin_bottom,
                                        'margin_left': margin_left, }, )
