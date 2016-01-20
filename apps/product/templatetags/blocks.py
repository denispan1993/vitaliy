# coding=utf-8
__author__ = 'Sergey'

from django_jinja.library import global_function
from django.template.loader import render_to_string


@global_function()
def many_blocks(blocks, request, category_or_product, top_border, limit_on_string=0, attachment='', ):
    # request_csrf_token = request.META.get(u"CSRF_COOKIE", None, )
    # request_csrf_token = request.COOKIES.get(u'csrftoken', None, )
    request_csrf_token = None
    template_name = u'category/templatetags/block_categories.jinja2'
    if category_or_product == 'product':
        from django.middleware.csrf import get_token
        request_csrf_token = get_token(request, )
        template_name = u'product/templatetags/block_products.jinja2'
    return render_to_string(template_name=template_name,
                            context={'blocks': blocks,
                                     'request': request,
                                     'csrf_token': request_csrf_token,
                                     'top_border': top_border,
                                     'limit_on_string': limit_on_string,
                                     'attachment': attachment, }, )


@global_function()
def one_block(block, request, choice, cycle, last_loop, category_or_product, ):
    from django.core.cache import cache
    key = 'one_block_%s_%d' % (category_or_product, block.pk, )
    this_one_block = cache.get(key=key, )
    if not this_one_block:
        if last_loop:
            margin_bottom = '0px'
        else:
            margin_bottom = '10px'
        if cycle == 1:
            margin_left = '0px'
        else:
            margin_left = '10px'
        template_name = u'product/templatetags/block_product.jinja2'
        if category_or_product == 'category':
            template_name = u'category/templatetags/block_category.jinja2'
        # elif category_or_product == 'product':
        #     template_name = u'product/templatetags/block_product.jinja2.html'
        from proj.settings import MEDIA_URL
        this_one_block = render_to_string(template_name=template_name,
                                          context={'block': block,
                                                   'request': request,
                                                   'MEDIA_URL': MEDIA_URL,
                                                   'choice': choice,
                                                   'margin_bottom': margin_bottom,
                                                   'margin_left': margin_left, }, )
        cache.set(key=key, value=this_one_block, timeout=120, )
    else:
        return this_one_block.decode('utf-8', )
    return this_one_block
