__author__ = 'Alex Starov'

from django_jinja.library import filter


@filter(name='int_to_string', )
def int_to_string(value, ):
    return str(value, )
