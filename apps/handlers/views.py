# coding=utf-8
__author__ = 'user'


def handler404(request, param=None,
               template_name=u'404.jinja2.html',
               ):
    from django.views.defaults import page_not_found
    page_not_found(request, )

    from django.template.loader import get_template
#    template_name = u'category/show_basement_category.jinja2.html'

    t = get_template(template_name)
    from django.template import RequestContext
    c = RequestContext(request, {u'param_dict': param, }, )
#    from django.template import Context
#    c = Context({'basement_categories': basement_categories, }, )
    html = t.render(c)
    from django.http import HttpResponse
    response = HttpResponse(html, )
#    from django.shortcuts import redirect
#    return redirect('/')
    # Мы не можем выяснить когда менялись внутринние подкатегории.
    # Поэтому мы не отдаем дату изменения текущей категории.
##    from apps.utils.datetime2rfc import datetime2rfc
##    response['Last-Modified'] = datetime2rfc(current_category.updated_at, )
    return response
