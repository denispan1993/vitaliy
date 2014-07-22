__author__ = 'Alex Starov'

from django_jinja.library import Library

register = Library()


@register.filter(name='formatted_float', )
def formatted_float(value, ):
    return str(value).replace(',', '.', )