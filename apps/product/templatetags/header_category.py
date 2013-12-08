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
        context = {'current_category': current_category, }
        return render_to_string(template_name=template_name, dictionary=context, )

    return _rendered(current_category=current_category, )
#    return {'current_category': current_category, }

# register.tag('templatetags_header_category/header_category.jinja2.html', header_category, )

@register.global_function()
def header_category2(current_category, product=None, ):

    root_string = u'<a href="/" title="Корень сайта">Home</a>'
    header_string = u'<a href="%s">%s</a>' % (current_category.get_absolute_url(),
                                              current_category.title, )
    next_category = current_category.parent
    while next_category:
        next_category_string = u'<a href="%s">%s</a>' % (next_category.get_absolute_url(),
                                                         next_category.title, )
        header_string = u'%s&nbsp;&gt;&nbsp;%s' % (next_category_string, header_string, )
        next_category = next_category.parent

    _string = u'%s&nbsp;&gt;&nbsp;%s' % (root_string, header_string, )
    if product:
        product_string = u'<a href="%s" title="%s">%s</a>' % (product.get_absolute_url(),
                                                              product.name,
                                                              product.title, )
        _string = u'%s&nbsp;&gt;&nbsp;%s' % (_string, product_string, )
    return _string
