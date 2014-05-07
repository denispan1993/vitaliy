__author__ = 'user'

from django_jinja.base import Library
#import jinja2

register = Library()


@register.filter(name='trim_whitespace', )
def trim(value, ):
    return value.strip()