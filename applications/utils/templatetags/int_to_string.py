# -*- coding: utf-8 -*-
from django_jinja.library import filter

__author__ = 'AlexStarov'


@filter(name='int_to_string', )
def int_to_string(value, ):
    return str(value, )
