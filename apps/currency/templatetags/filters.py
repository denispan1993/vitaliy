# coding=utf-8
__author__ = 'Sergey'

from django_jinja.library import Library
from django.template.loader import render_to_string

register = Library()

"""
Конвертируем значение value в нужную нам валюту
"""
@register.filter()
def convert_currency(value, request, *args, **kwargs):
    current_currency = request.session.get(u'currency_pk', None, )
    if current_currency:
        try:
            current_currency = int(current_currency, )
        except ValueError:
            current_currency = 1
    else:
        current_currency = 1
    if current_currency == 1:
        ''' Если текущая валюта сайта "Гривна":
            Возвращаем полученое значени
        '''
        return value
    else:
        if value:
            try:
                value = int(value, )
            except ValueError:
                value = 0
        else:
            value = 0
        from apps.product.models import Currency
        try:
            current_currency = Currency.objects.get(pk=current_currency, )
        except Currency.DoesNotExist:
            pass
        else:
            ''' Приводим к нужной валюте:
                1. умножаем на количество гривен
                2. делим на курс
            '''
            return str(value*current_currency.currency/current_currency.exchange_rate)