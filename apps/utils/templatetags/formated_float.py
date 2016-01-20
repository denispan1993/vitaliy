# -*- coding: utf-8 -*-
__author__ = 'AlexStarov'

from django_jinja.library import filter


@filter(name='formatted_float', )
def formatted_float(value, ):
    return str(value).replace(',', '.', )