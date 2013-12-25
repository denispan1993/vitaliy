# coding=utf-8
__author__ = 'Sergey'

from django_jinja.library import Library
from django.template.loader import render_to_string

register = Library()


@register.global_function()
def block_categories(categories, request, ):
    return render_to_string(template_name=u'category/templatetags/block_categories.jinja2.html',
                            dictionary={'categories': categories,
                                        'request': request, }, )


@register.global_function()
def block_category(category, cycle, ):
    if cycle == 1:
        category_block = 'first_category_block'
    else:
        category_block = 'category_block'
    return render_to_string(template_name=u'category/templatetags/block_category.jinja2.html',
                            dictionary={'category': category,
                                        'category_block': category_block, }, )


@register.global_function()
def this_category(category, ):
    return render_to_string(template_name=u'category/templatetags/this_category.jinja2.html',
                            dictionary={'category': category, }, )
