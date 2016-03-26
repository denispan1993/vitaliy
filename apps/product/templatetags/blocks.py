# -*- coding: utf-8 -*-
from django_jinja.library import global_function
from django.template.loader import render_to_string

__author__ = 'AlexStarov'


@global_function()
def many_blocks(blocks, request, category_or_product, top_border, limit_on_string=0, attachment='', ):

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

    margin_bottom = '10px'
    if last_loop:
        margin_bottom = '0px'

    margin_left = '10px'
    if cycle == 1:
        margin_left = '0px'

    key = 'one_block_%s_%d_%s_%s_%s_%s' % (
        category_or_product,
        block.pk,
        request.session.get(u'currency_pk', ),
        choice,
        margin_bottom,
        margin_left,
    )

    from django.core.cache import cache
    this_one_block = cache.get(key=key, )

    if this_one_block:
        return this_one_block.decode('utf-8', )

    else:
        template_name = u'product/templatetags/block_product.jinja2'
        if category_or_product == 'category':
            template_name = u'category/templatetags/block_category.jinja2'

        from proj.settings import MEDIA_URL
        this_one_block = render_to_string(template_name=template_name,
                                          context={'block': block,
                                                   'request': request,
                                                   'MEDIA_URL': MEDIA_URL,
                                                   'choice': choice,
                                                   'margin_bottom': margin_bottom,
                                                   'margin_left': margin_left, }, )

        cache.set(key=key, value=this_one_block, timeout=600, )
        return this_one_block
