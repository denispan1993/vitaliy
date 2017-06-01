# -*- coding: utf-8 -*-
from django_jinja.library import filter
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
import re

__author__ = 'AlexStarov'


@filter(name='trim_whitespace', )
def trim(value, ):
    return value.strip()


@filter(name='spacify', )
def spacify(value, autoescape=None):
    if autoescape:
        esc = conditional_escape
    else:
        esc = lambda x: x
    return mark_safe(re.sub('\s', '&'+'nbsp;', esc(value)))

spacify.needs_autoescape = True
