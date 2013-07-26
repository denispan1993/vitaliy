# coding=utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext


def show_static_page(request,
                     static_page_url,
                     template_name=u'static_page.jinja2.html', ):
    from apps.static.models import Static
    try:
        static_page = Static.objects.get(url=static_page_url, )
    except Static.DoesNotExist:
        from django.http import Http404
        raise Http404

    return render_to_response(template_name=template_name,
                              {'static_page': static_page, },
                              context_instance=RequestContext(request, ),
                              content_type='text/html', )
