# -*- coding: utf-8 -*-
__author__ = 'AlexStarov'

from django.shortcuts import render


def show_static_page(request,
                     static_page_url,
                     template_name=u'static_page.jinja2', ):
    from applications.static.models import Static
    try:
        page = Static.objects.get(url=static_page_url, )
    except Static.DoesNotExist:
        from django.http import Http404
        raise Http404
    import markdown
    if page:
        html_text = markdown.markdown(page.text, )
    else:
        html_text = None
    response = render(request=request,
                      template_name=template_name,
                      context={'page': page,
                               'html_text': html_text, },
                      content_type='text/html', )
    # from datetime import datetime
    from applications.utils.datetime2rfc import datetime2rfc
    response['Last-Modified'] = datetime2rfc(page.updated_at, )
    return response
