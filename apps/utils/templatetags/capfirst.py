__author__ = 'Alex Starov'

from django_jinja.library import Library

register = Library()


@register.filter(name='capfirst', )
def up_first_letter(value, ):
    first = value[0] if len(value) > 0 else ''
    remaining = value[1:] if len(value) > 1 else ''
    return first.upper() + remaining