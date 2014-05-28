__author__ = 'user'

from django_jinja.base import Library
#import jinja2

register = Library()


@register.filter(name='int_to_string', )
def int_to_string(value, ):
    return str(value, )