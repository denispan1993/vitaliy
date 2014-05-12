# coding=utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext


def order_search(request,
                 template_name=u'order/order_search.jinja2.html', ):
    if request.method == 'POST':
        POST_NAME = request.POST.get(u'POST_NAME', None, )
        if POST_NAME == 'order_search':
            order_id = request.POST.get(u'order_id', None, )
    else:
        response = render_to_response(template_name=template_name,
    #                                  dictionary={'page': page,
    #                                              'html_text': html_text, },
                                      context_instance=RequestContext(request, ),
                                      content_type='text/html', )
    # from datetime import datetime
#    from apps.utils.datetime2rfc import datetime2rfc
#    response['Last-Modified'] = datetime2rfc(page.updated_at, )
    return response


def order_edit(request,
               id,
               template_name=u'order/order_edit.jinja2.html', ):
#    from apps.static.models import Static
#    try:
#        page = Static.objects.get(url=static_page_url, )
#    except Static.DoesNotExist:
#        from django.http import Http404
#        raise Http404
#    import markdown
#    if page:
#        html_text = markdown.markdown(page.text, )
#    else:
#        html_text = None
    response = render_to_response(template_name=template_name,
#                                  dictionary={'page': page,
#                                              'html_text': html_text, },
                                  context_instance=RequestContext(request, ),
                                  content_type='text/html', )
    # from datetime import datetime
#    from apps.utils.datetime2rfc import datetime2rfc
#    response['Last-Modified'] = datetime2rfc(page.updated_at, )
    return response