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
    if value:
        ''' Сначала преобразуем value в число
        '''
        try:
            value = int(value, )
        except ValueError:
            value = 0
    else:
        value = 0
    current_currency = request.session.get(u'currency_pk', None, )
    if current_currency:
        ''' Теперь преобразуем сосбственно код валюты сайта
         '''
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
        pass
        # return value
    else:
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
            # return str(value*current_currency.currency/current_currency.exchange_rate)
            value = value*current_currency.currency/current_currency.exchange_rate
    return u'%5.2f'.replace(',', '.', ) % value