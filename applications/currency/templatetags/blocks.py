# -*- coding: utf-8 -*-
from django_jinja.library import global_function # import library
from django.core.cache import cache

from applications.product.models import Currency

__author__ = 'AlexStarov'


@global_function()
def get_currency(request, ):

    current_currency = request.session.get(u'currency_pk', )

    if current_currency:
        currency_all = cache.get(key='currency_all', )
        return currency_all.filter(pk=current_currency)[0].name_truncated
        #try:
        #    return Currency.objects\
        #        .values_list('name_truncated', flat=True)\
        #        .get(pk=current_currency, )
        #except Currency.DoesNotExist:
        #    pass

    return u'грн.'


@global_function()
def get_currency_ISO(request, ):

    current_currency = request.session.get(u'currency_pk', )

    if current_currency:

        try:
            return Currency.objects\
                .values_list('currency_code_ISO_char', flat=True)\
                .get(pk=current_currency, )
        except Currency.DoesNotExist:
            pass

    return 'UAH'
