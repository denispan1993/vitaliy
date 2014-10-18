#coding=utf-8
__author__ = 'Alex Starov'

from django_jinja.library import Library

register = Library()


@register.filter(name='true_false', )
def true_false(value, ):
    if bool(value):
        if value is True:
            return u'Да'
        elif value is False:
            return u'Нет'
    else:
        return False
