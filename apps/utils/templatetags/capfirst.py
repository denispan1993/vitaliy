# -*- coding: utf-8 -*-
__author__ = 'AlexStarov'

from django_jinja.library import filter


@filter(name='capfirst', )
def up_first_letter(value, ):
    first = value[0] if len(value) > 0 else ''
    remaining = value[1:] if len(value) > 1 else ''
    return first.upper() + remaining