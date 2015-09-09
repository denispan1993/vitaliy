# coding=utf-8
__author__ = 'Sergey'

from django_jinja.library import global_function
from django.template.loader import render_to_string


@global_function()
def block_categories(categories, request, ):
    return render_to_string(template_name=u'category/templatetags/block_categories.jinja2.html',
                            dictionary={'categories': categories,
                                        'request': request, }, )


@global_function()
def block_category(category, cycle, ):
    if cycle == 1:
        category_block_margin = '0 0 10px 0px;'
    else:
        category_block_margin = '0 0 10px 10px;'
    return render_to_string(template_name=u'category/templatetags/block_category.jinja2.html',
                            dictionary={'category': category,
                                        'category_block_margin': category_block_margin, }, )


@global_function()
def this_category(category, width_this_category, ):
    # print(width_this_category)
    return render_to_string(template_name=u'category/templatetags/this_category.jinja2.html',
                            dictionary={'category': category,
                                        'width_this_category': width_this_category, }, )
