# -*- coding: utf-8 -*-
from django_jinja.library import filter

__author__ = 'AlexStarov'


@filter(name='custom_filter', )
def custom_filter(value, ):
    return type(value, )
