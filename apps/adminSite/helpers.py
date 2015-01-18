# coding=utf-8
__author__ = 'Sergey'

from django.template.loader import render_to_string

from jingo import register


@register.filter()
def true_false(value, ):
        if value:
            return u'Да'
        elif not value:
            return u'Нет'
        else:
            return u'Что-то ещё'


@register.filter()
def int_to_string(value, ):
    return str(value, )


@register.filter()
def get_range(value, ):
    """
    Filter - returns a list containing range made from given value
    Usage (in template):

    <ul>{% for i in 3|get_range %}
      <li>{{ i }}. Do something</li>
    {% endfor %}</ul>

    Results with the HTML:
    <ul>
      <li>0. Do something</li>
      <li>1. Do something</li>
      <li>2. Do something</li>
    </ul>

    Instead of 3 one may use the variable set in the views
    """
    return range(value, )


@register.function()
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
