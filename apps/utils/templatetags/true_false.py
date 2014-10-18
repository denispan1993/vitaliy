#coding=utf-8
__author__ = 'Alex Starov'

from django_jinja.library import Library

register = Library()


@register.filter(name='true_false', )
def true_false(value, ):
#    if bool(value):
        if value:
            return u'Да'
        elif not value:
            return u'Нет'
        else:
            return u'Что-то ещё'
#    else:
#        return str(value)
