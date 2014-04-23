__author__ = 'user'

from django_jinja.base import Library
#import jinja2

register = Library()


@register.filter(name='custom_QuerySet_filter', )
def custom_QuerySet_filter(value, filter_sting, ):
    value = value.filter(filter_sting, )  # is_availability=1)
    return value