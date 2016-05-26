# -*- coding: utf-8 -*-
from django_jinja.library import global_function
from django.template.loader import render_to_string
from django.core.cache import cache
from logging import getLogger
import hashlib

__author__ = 'AlexStarov'

logging = getLogger('proj.processor.request_Middleware')


@global_function()
def many_blocks(blocks, request, category_or_product, top_border, limit_on_string=0, attachment='', ):

    request_csrf_token = None
    template_name = u'category/templatetags/block_categories.jinja2'

    if category_or_product == 'product':
        from django.middleware.csrf import get_token
        request_csrf_token = get_token(request, )
        template_name = u'product/templatetags/block_products.jinja2'

    key = '%s_block_' % ('prod' if category_or_product == 'product' else 'cat', )

    for block in blocks:
        key += '_%s' % str(block.pk)

    key += '__currency_pk_%s' % request.session.get(u'currency_pk', )

    if top_border:
        key += '__top_border'

    if limit_on_string == 0:
        limit_on_string = request.session.limit_on_string

    key += '__limit_on_string_%s' % str(limit_on_string)

    if attachment:
        key += '__attachment_%s' % attachment

    logging.debug('blocks: key for cache: {0}'.format(key))

    m = hashlib.md5(key)

    md5_key = '%s_blocks_%s' % (
        'prod' if category_or_product == 'product' else 'cat',
        m.hexdigest(), )

    logging.debug('blocks: key for cache (MD5): {0}'.format(md5_key))

    block = cache.get(key=md5_key, )
    if block:
        logging.debug('blocks: cache successful: YES')
    else:
        cache.set(key=md5_key, value='YES', timeout=900)
        logging.debug('blocks: cache successful: NO')


    return render_to_string(template_name=template_name,
                            context={'blocks': blocks,
                                     'category_or_product': category_or_product,
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

    key = '%s_block_' % ('prod' if category_or_product == 'product' else 'cat', )

    key += '%d_%s_%s_%s_%s' % (
        block.pk,
        request.session.get(u'currency_pk', ),
        choice,
        margin_bottom,
        margin_left,
    )

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

        cache.set(key=key, value=this_one_block, timeout=900, )
        return this_one_block
