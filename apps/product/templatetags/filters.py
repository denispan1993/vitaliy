# -*- coding: utf-8 -*-
from django_jinja.library import filter
from django_jinja.library import global_function

__author__ = 'AlexStarov'


@filter(name='truncatechar', )
def truncatechar(value, arg, ):
    if len(str(value, ), ) < arg:
        return value
    else:
        return value[:arg]


@global_function(name='dprint', )
def dprint(name, value, ):
    print name, value
