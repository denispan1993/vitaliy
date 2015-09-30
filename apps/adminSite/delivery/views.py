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
            print 'Test: ', test
            if test == None:
                print 'Test: None'
                test = True
            else:
                if isinstance(test, unicode, ):
                    try:
                        test = int(test, )
                    except Exception as inst:
                        print inst
                        print type(inst, )
                        print inst.args
                        test = True
                    else:
                        test = bool(test, )
                else:
                    print 'Test: Not unicode'
                    test = True
            send_test = request.POST.get(u'send_test', None, )
            if send_test == None:
                send_test = True
            else:
                if isinstance(send_test, unicode, ):
                    try:
                        send_test = int(send_test, )
                    except Exception as inst:
                        send_test = True
                    else:
                        send_test = bool(send_test, )
                else:
                    send_test = True
            send_general = request.POST.get(u'send_general', None, )
            if send_general == None:
                send_general = True
            else:
                if isinstance(send_general, unicode, ):
                    try:
                        send_general = int(send_general, )
                    except Exception as inst:
                        send_general = True
                    else:
                        send_general = bool(send_general, )
                else:
                    send_general = True
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
            # if delivery_pk == delivery_id:
            #     print 'delivery_id', delivery_id, 'delivery_pk', delivery_pk
            # else:
            #     print 'delivery_id', delivery_id, 'delivery_pk', delivery_pk
            try:
            #    print delivery_pk
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
            delivery.send_test = send_test
            delivery.send_general = send_general
            # print test
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

@staff_member_required
def start_delivery(request,
                   delivery_id=None,
                   delivery_type='test',
                   template_name=None, ):
    from django.shortcuts import redirect
    if request.method == "POST":
        POST_NAME = request.POST.get(u'POST_NAME', None, )
        # if POST_NAME in ('start_delivery_test', 'start_delivery_general'):
        if POST_NAME == 'start_delivery_test':
            if delivery_id:
                try:
                    delivery_id = int(delivery_id, )
                except ValueError:
                    """ Уже РЕДИРЕКТ отсюда """
                    error_message = u'Отсутвует номер рассылки'
                    return redirect(to='admin_delivery:index', )
                else:
                    from apps.delivery.models import Delivery
                    try:
                        delivery = Delivery.objects.get(pk=delivery_id, )
                    except Delivery.DoesNotExist:
                        error_message = u'В базе отсутсвует рассылка с таким номером.'
                        return redirect(to='admin_delivery:index', )
                    else:
                        from django.core.management import call_command
                        if POST_NAME == 'start_delivery_test' and delivery_type == 'test' and not delivery.send_test:
                            call_command(name='processing_delivery_send',
                                         delivery_pk=delivery_id,
                                         delivery_test=True,
                                         delivery_general=False, )
                        #elif POST_NAME == 'start_delivery_general' and delivery_type == 'general' and not delivery.send_general:
                        #    call_command(name='processing_delivery_send',
                        #                 delivery_pk=delivery_id,
                        #                 delivery_test=False,
                        #                 delivery_general=True, )

    return redirect(to='admin_delivery:index', )
