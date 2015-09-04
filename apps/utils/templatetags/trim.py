__author__ = 'Alex Starov'

from django_jinja.library import filter


@filter(name='trim_whitespace', )
def trim(value, ):
    return value.strip()