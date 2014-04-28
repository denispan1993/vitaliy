__author__ = 'user'

from django_jinja.base import Library
#import jinja2

register = Library()


@register.filter(name='custom_QuerySet_filter', )
def custom_QuerySet_filter(value, variable, operation, value_variable, ):
    value = value.filter(is_availability=1, )  # map(variable, operation, value_variable, ), )  # is_availability=1)
    return value