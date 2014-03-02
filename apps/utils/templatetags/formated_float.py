__author__ = 'user'

from django_jinja.base import Library

register = Library()


@register.filter(name='formatted_float', )
def formatted_float(value, ):
    return str(value).replace(',', '.', )