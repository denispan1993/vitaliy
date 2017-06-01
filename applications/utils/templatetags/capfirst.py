# -*- coding: utf-8 -*-
from django_jinja.library import filter

__author__ = 'AlexStarov'


@filter(name='capfirst', )
def up_first_letter(value, ):
    first = value[0] if len(value) > 0 else ''
    remaining = value[1:] if len(value) > 1 else ''
    return first.upper() + remaining