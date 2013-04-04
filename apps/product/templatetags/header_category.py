# coding=utf-8

__author__ = 'Sergey'

from django import template

register = template.Library()

@register.inclusion_tag('templatetags_header_category/header_category.html', )
def header_category(current_category, ):
    return {'current_category': current_category, }