# coding=utf-8

__author__ = 'Sergey'

#from django.template import Library
from django_jinja.library import global_function
from django.template.loader import render_to_string


#@register.inclusion_tag('templatetags_header_category/header_category.jinja2.html', )
@global_function()
def header_category(current_category, ):

    def _rendered(current_category):
        template_name = u'templatetags_header_category/header_category.jinja2.html'
        context = {'current_category': current_category, }
        return render_to_string(template_name=template_name, dictionary=context, )

    return _rendered(current_category=current_category, )
#    return {'current_category': current_category, }

# register.tag('templatetags_header_category/header_category.jinja2.html', header_category, )


@global_function()
def header_category_billboard(current_category, product=None, ):

    if product:
        _end_string = u'<li class="category"><a href="%s">%s</a></li>' % \
                      (current_category.get_absolute_url(),
                       current_category.title,)
    else:
        _end_string = u'<li class="current_category">%s</li>' % current_category.title

    _intermediate_string = ''
    next_category = current_category.parent
    while next_category:
        _previous_category_string = u'<li><a href="%s">%s</a><span>&nbsp;/&nbsp;</span></li>' %\
                                    (next_category.get_absolute_url(),
                                     next_category.title, )
        _intermediate_string = u'%s%s' % (_previous_category_string, _intermediate_string, )
        next_category = next_category.parent

    _string = u'%s%s' % (_intermediate_string, _end_string, )
    if product:
        product_string = u'<li class="product"><span>&nbsp;/&nbsp;</span><a href="%s" title="%s">%s</a></li>' % (product.get_absolute_url(),
                                                              product.name,
                                                              product.title, )
        _string = u'%s%s' % (_string, product_string, )
    return _string
