# coding=utf-8

__author__ = 'Sergey'

from django.template import Library
#from coffin.template import Library

register = Library()

@register.inclusion_tag('templatetags_header_category/header_category.html', )
def header_category(current_category, ):
    return {'current_category': current_category, }

# register.tag('templatetags_header_category/header_category.html', header_category, )
