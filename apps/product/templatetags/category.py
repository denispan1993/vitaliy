# coding=utf-8
__author__ = 'Sergey'

from django_jinja.library import Library
from django.template.loader import render_to_string

register = Library()

@register.global_function()
def category(category, ):
    return render_to_string(template_name=u'category/templatetags/category.jinja2.html', dictionary={'category': category, }, )
