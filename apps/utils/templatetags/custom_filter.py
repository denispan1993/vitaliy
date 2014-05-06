__author__ = 'user'

from django_jinja.base import Library
#import jinja2

register = Library()


@register.filter(name='custom_filter', )
def custom_filter(value, ):
    return type(value)