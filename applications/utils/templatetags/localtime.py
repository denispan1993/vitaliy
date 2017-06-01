# -*- coding: utf-8 -*-
from django_jinja.library import filter
from django.utils import timezone

__author__ = 'AlexStarov'


@filter(name='to_localtime', )
def localtime(value, ):
    return timezone.localtime(value, )
