# -*- coding: utf-8 -*-
__author__ = 'AlexStarov'

from django_jinja.library import filter


@filter(name='int_to_string', )
def int_to_string(value, ):
    return str(value, )
