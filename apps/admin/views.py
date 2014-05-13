# coding=utf-8


def order_search(request,
                 template_name=u'order/order_search.jinja2.html', ):
    if request.method == 'POST':
        POST_NAME = request.POST.get(u'POST_NAME', None, )
        if POST_NAME == 'order_search':
            order_id = request.POST.get(u'order_id', None, )
            if order_id:
                try:
                    order_id = int(order_id, )
                except ValueError:
                    error_message = u'Некорректно введен номер заказа.'
                else:
                    order_id = '%06d' % order_id
                    from django.shortcuts import redirect
                    return redirect(to='order_edit', id=order_id, )
    else:
        error_message = u''
    # from datetime import datetime
#    from apps.utils.datetime2rfc import datetime2rfc
#    response['Last-Modified'] = datetime2rfc(page.updated_at, )
    from apps.cart.models import Order
    order = Order.objects.all()
    from django.shortcuts import render_to_response
    from django.template import RequestContext
    response = render_to_response(template_name=template_name,
                                  dictionary={'error_message': error_message,
                                              'order': order, },  # 'html_text': html_text, },
                                  context_instance=RequestContext(request, ),
                                  content_type='text/html', )
    return response


def order_edit(request,
               id,
               template_name=u'order/order_edit.jinja2.html', ):
    if id:
        try:
            order_id = int(id, )
        except ValueError:
            error_message = u'Некорректно введен номер заказа.'
            from django.shortcuts import redirect
            return redirect(to='order_search', )
        else:
            from apps.cart.models import Order
            order = Order.objects.get(pk=id, )
    else:
        error_message = u'Отсутсвует номер заказа.'
        from django.shortcuts import redirect
        return redirect(to='order_search', )

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
    from django.shortcuts import render_to_response
    from django.template import RequestContext
    response = render_to_response(template_name=template_name,
                                  dictionary={'order_id': id,
                                              'order': order, },
                                  context_instance=RequestContext(request, ),
                                  content_type='text/html', )
    # from datetime import datetime
    # from apps.utils.datetime2rfc import datetime2rfc
    # response['Last-Modified'] = datetime2rfc(page.updated_at, )
    return response