# coding=utf-8
__author__ = 'Sergey'

from django_jinja.library import Library
from django.template.loader import render_to_string

register = Library()


@register.global_function()
def get_currency(request, ):
    current_currency = request.session.get(u'currency_pk', )
    return_str = u'грн.'
    if current_currency:
        from apps.product.models import Currency
        try:
            current_currency = int(current_currency, )
        except ValueError:
            current_currency = 1
        try:
            current_currency = Currency.objects.get(pk=current_currency, )
        except Currency.DoesNotExist:
            pass
        else:
            return_str = current_currency.name_truncated
    return return_str


#@register.global_function()
#def convert_currency(request, ):
#    current_currency = request.session.get(u'currency_pk', )
#    return_str = u'грн.'
#    if current_currency:
#        from apps.product.models import Currency
#        try:
#            current_currency = int(current_currency, )
#        except ValueError:
#            current_currency = 1
#        try:
#            current_currency = Currency.objects.get(pk=current_currency, )
#        except Currency.DoesNotExist:
#            pass
#        else:
#            return_str = current_currency.name_truncated
#    return return_str

