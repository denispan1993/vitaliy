# -*- coding: utf-8 -*-
__author__ = 'AlexStarov'

from django_jinja.library import filter


@filter(name='trim_whitespace', )
def trim(value, ):
    return value.strip()
