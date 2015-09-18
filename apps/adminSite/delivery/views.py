# -*- coding: utf-8 -*-
__author__ = 'Alex Starov'

from django.contrib.admin.views.decorators import staff_member_required


@staff_member_required
def index(request,
          template_name=u'delivery/index.jinja2.html', ):
    error_message = u''
    if request.method == 'POST':
        POST_NAME = request.POST.get(u'POST_NAME', None, )
        if POST_NAME == 'index':
            id = request.POST.get(u'id', None, )
            if id:
                try:
                    id = int(id, )
                except ValueError:
                    error_message = u'Некорректно введен номер Рассылки.'
                else:
                    from apps.delivery.models import Delivery
                    if Delivery.objects.get(pk=id, ).exists():
                        id = '%06d' % id
                        from django.shortcuts import redirect
                        return redirect(to='admin_delivery:edit', id=id, )
                    else:
                        error_message = u'Рассылка с таким номером не существует.'
    # from datetime import datetime
#    from apps.utils.datetime2rfc import datetime2rfc
#    response['Last-Modified'] = datetime2rfc(page.updated_at, )
    from datetime import datetime, timedelta
    filter_datetime = datetime.now() - timedelta(days=93, )
    # print filter_datetime
    from apps.delivery.models import Delivery
    mailings = Delivery.objects.filter(created_at__gte=filter_datetime, )
    from django.shortcuts import render_to_response
    from django.template import RequestContext
    response = render_to_response(template_name=template_name,
                                  dictionary={'error_message': error_message,
                                              'mailings': mailings, },  # 'html_text': html_text, },
                                  context_instance=RequestContext(request, ),
                                  content_type='text/html', )
    return response


@staff_member_required
def add_edit(request,
             delivery_id=None,
             template_name=u'delivery/add_edit.jingo.html', ):
    if request.method == "POST":
        POST_NAME = request.POST.get(u'POST_NAME', None, )
        if POST_NAME == 'add_edit':
            name = request.POST.get(u'name', None, )
            if not name:
                name = 'Имя рассылки'
            test = request.POST.get(u'test', None, )
            if test == None:
                print 'None'
                test = False
            delivery_type = request.POST.get(u'type', None, )
            if delivery_type == None:
                delivery_type = 1
            else:
                try:
                    delivery_type = int(delivery_type, )
                except ValueError:
                    delivery_type = 1
            subject = request.POST.get(u'subject', None, )
            html = request.POST.get(u'html', None, )
            """ Проверяем, это новая рассылка?
                Или отредактированная старая? """
            from apps.delivery.models import Delivery
            delivery_pk = request.POST.get(u'delivery_pk', None, )
            if delivery_pk == delivery_id:
                print 'delivery_id', delivery_id, 'delivery_pk', delivery_pk
            else:
                print 'delivery_id', delivery_id, 'delivery_pk', delivery_pk
            try:
                print delivery_pk
                delivery_pk = int(delivery_pk, )
            except (ValueError, TypeError):
                """ Новая """
                delivery = Delivery()
            else:
                """ Отредактированная - старая """
                try:
                    delivery = Delivery.objects.get(pk=delivery_pk, )
                except Delivery.DoesNotExist:
                    from django.shortcuts import redirect
                    return redirect(to='admin_delivery:index', )

            delivery.name = name
            delivery.delivery_test = test
            print test
            delivery.type = delivery_type
            delivery.subject = subject
            delivery.html = html
            delivery.save()
            from django.shortcuts import redirect
            return redirect(to='admin_delivery:index', )

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
    from apps.delivery.models import Delivery
    type_mailings = Delivery.Type_Mailings
    from django.shortcuts import render_to_response
    from django.template import RequestContext
    from apps.delivery.forms import DeliveryCreateEditForm
    response = render_to_response(template_name=template_name,
                                  dictionary={'delivery_id': delivery_id,
                                              'delivery': delivery,
                                              'type_mailings': type_mailings,
                                              'form': DeliveryCreateEditForm, },
                                  context_instance=RequestContext(request, ),
                                  content_type='text/html', )
    # from datetime import datetime
    # from apps.utils.datetime2rfc import datetime2rfc
    # response['Last-Modified'] = datetime2rfc(page.updated_at, )
    return response
