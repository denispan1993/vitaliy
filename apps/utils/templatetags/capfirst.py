__author__ = 'user'

from django_jinja.base import Library
#import jinja2

register = Library()


@register.filter(name='capfirst', )
def up_first_letter(value):
    first = value[0] if len(value) > 0 else ''
    remaining = value[1:] if len(value) > 1 else ''
    return first.upper() + remaining