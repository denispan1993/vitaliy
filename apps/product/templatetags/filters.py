# -*- coding: utf-8 -*-
from logging import getLogger
from django_jinja.library import filter
from django_jinja.library import global_function

__author__ = 'AlexStarov'

debug_log = getLogger('debug')


@filter(name='truncatechar', )
def truncatechar(value, arg, ):
    if len(str(value, ), ) < arg:
        return value
    else:
        return value[:arg]


@global_function(name='dprint', )
def dprint(name, value, ):
    pass
    # debug_log.info('name: {0}, value: {1}'.format(name, value, ), )
