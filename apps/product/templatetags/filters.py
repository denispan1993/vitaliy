# -*- coding: utf-8 -*-
#from libxml2mod import name
__author__ = 'user'

from django_jinja.base import Library
#import jinja2

register = Library()

@register.filter(name='formatted_float', )
#@jinja2.contextfilter
def formatted_float(value, ):
    return str(value).replace(',', '.', )

@register.filter(name='truncatechar', )
# truncate after a certain number of characters
def truncatechar(value, arg, ):
    if len(str(value, ), ) < arg:
        return value
    else:
        return value[:arg]

#register.filter('formatted_float', formatted_float)

#@register.global_context
#def hello(name):
#    return "Hello" + name
