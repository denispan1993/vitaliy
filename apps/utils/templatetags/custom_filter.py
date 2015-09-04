__author__ = 'Alex Starov'

from django_jinja.library import filter


@filter(name='custom_filter', )
def custom_filter(value, ):
    return type(value)