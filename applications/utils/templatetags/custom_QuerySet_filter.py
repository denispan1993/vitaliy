# -*- coding: utf-8 -*-
from django_jinja.library import filter

__author__ = 'AlexStarov'


@filter(name='custom_QuerySet_filter', )
def custom_QuerySet_filter(value, variable, operation, value_variable, ):
    value = value.filter(is_availability=1, )  # map(variable, operation, value_variable, ), )  # is_availability=1)
    return value
