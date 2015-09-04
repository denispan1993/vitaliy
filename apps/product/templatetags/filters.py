# -*- coding: utf-8 -*-
#from libxml2mod import name
__author__ = 'user'

from django_jinja.library import filter


@filter(name='truncatechar', )
def truncatechar(value, arg, ):
    if len(str(value, ), ) < arg:
        return value
    else:
        return value[:arg]
