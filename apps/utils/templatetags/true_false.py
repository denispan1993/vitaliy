# -*- coding: utf-8 -*-
#from django_jinja.library import Library
from django_jinja.library import filter

__author__ = 'AlexStarov'

#register = Library()


#@register.filter(name='true_false', )
@filter(name='true_false', )
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
