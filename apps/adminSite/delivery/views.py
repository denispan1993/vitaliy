# -*- coding: utf-8 -*-
__author__ = 'Alex Starov'

from django.contrib.admin.views.decorators import staff_member_required


@staff_member_required
def index(request,
          template_name=u'delivery/index.jingo.html', ):
    error_message = u''
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
                    from apps.cart.models import Order
                    try:
                        order = Order.objects.get(pk=order_id, )
                    except Order.DoesNotExist:
                        error_message = u'Заказа с таким номером не существует.'
                    else:
                        order_id = '%06d' % order_id
                        from django.shortcuts import redirect
                        return redirect(to='order_edit', id=order_id, )
    # from datetime import datetime
#    from apps.utils.datetime2rfc import datetime2rfc
#    response['Last-Modified'] = datetime2rfc(page.updated_at, )
    from datetime import datetime, timedelta
    filter_datetime = datetime.now() - timedelta(days=31, )
    # print filter_datetime
    from apps.cart.models import Order
    orders = Order.objects.filter(created_at__gte=filter_datetime, )
    from django.shortcuts import render_to_response
    from django.template import RequestContext
    response = render_to_response(template_name=template_name,
                                  dictionary={'error_message': error_message,
                                              'orders': orders, },  # 'html_text': html_text, },
                                  context_instance=RequestContext(request, ),
                                  content_type='text/html', )
    return response


@staff_member_required
def edit(request,
         order_id,
         template_name=u'delivery/edit.jingo.html', ):
    from django.shortcuts import redirect
    if order_id:
        try:
            order_id = int(order_id, )
        except ValueError:
            error_message = u'Некорректно введен номер заказа.'
            return redirect(to='order_search', )
        else:
            from apps.cart.models import Order
            try:
                order = Order.objects.get(pk=order_id, )
            except Order.DoesNotExist:
                error_message = u'В базе отсутсвует заказ с таким номером.'
                return redirect(to='order_search', )
    else:
        error_message = u'Отсутсвует номер заказа.'
        return redirect(to='order_search', )

    from django.shortcuts import render_to_response
    from django.template import RequestContext
    response = render_to_response(template_name=template_name,
                                  dictionary={'order_id': order_id,
                                              'order': order, },
                                  context_instance=RequestContext(request, ),
                                  content_type='text/html', )
    # from datetime import datetime
    # from apps.utils.datetime2rfc import datetime2rfc
    # response['Last-Modified'] = datetime2rfc(page.updated_at, )
    return response


@staff_member_required
def add_edit(request,
             delivery_id=None,
             template_name=u'delivery/add_edit.jingo.html', ):
    from django.shortcuts import redirect
    if delivery_id:
        try:
            delivery_id = int(delivery_id, )
        except ValueError:
            error_message = u'Некорректно введен номер рассылки.'
            return redirect(to='admin_delivery:index', )
        else:
            from apps.delivery.models import Delivery
            try:
                delivery = Delivery.objects.get(pk=delivery_id, )
            except Delivery.DoesNotExist:
                error_message = u'В базе отсутсвует рассылка с таким номером.'
                return redirect(to='admin_delivery:index', )
    else:
        delivery = None
    from django.shortcuts import render_to_response
    from django.template import RequestContext
    from apps.delivery.forms import DeliveryCreateEditForm
    response = render_to_response(template_name=template_name,
                                  dictionary={'delivery_id': delivery_id,
                                              'delivery': delivery,
                                              'form': DeliveryCreateEditForm, },
                                  context_instance=RequestContext(request, ),
                                  content_type='text/html', )
    # from datetime import datetime
    # from apps.utils.datetime2rfc import datetime2rfc
    # response['Last-Modified'] = datetime2rfc(page.updated_at, )
    return response
