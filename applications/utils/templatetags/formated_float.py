# -*- coding: utf-8 -*-
from django_jinja.library import filter

__author__ = 'AlexStarov'


@filter(name='formatted_float', )
def formatted_float(value, ):
    return str(value).replace(',', '.', )