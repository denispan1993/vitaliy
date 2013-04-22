# coding=utf-8

__author__ = 'Sergey'

#from django.template import Library
from django_jinja.library import Library
from django.template.loader import render_to_string


register = Library()

#@register.inclusion_tag('templatetags_header_category/header_category.jinja2.html', )
@register.global_function()
def header_category(current_category, ):

    def _rendered(current_category):
        template_name = u'templatetags_header_category/header_category.jinja2.html'
        context ={'current_category': current_category, }
        return render_to_string(template_name=template_name, dictionary=context, )

    return _rendered(current_category=current_category, )
#    return {'current_category': current_category, }

# register.tag('templatetags_header_category/header_category.jinja2.html', header_category, )
