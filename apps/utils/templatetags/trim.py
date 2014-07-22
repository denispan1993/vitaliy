__author__ = 'Alex Starov'

from django_jinja.library import Library

register = Library()


@register.filter(name='trim_whitespace', )
def trim(value, ):
    return value.strip()