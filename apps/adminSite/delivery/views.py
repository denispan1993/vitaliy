# -*- coding: utf-8 -*-
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from django.core.management import call_command

from apps.authModel.models import Email
from apps.delivery.models import Delivery, Email_Img, SpamEmail
from apps.delivery.forms import DeliveryCreateEditForm
from apps.delivery.tasks import processing_delivery

__author__ = 'AlexStarov'


@staff_member_required
def index(request,
          template_name=u'delivery/index.jinja2', ):
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
                    if Delivery.objects.get(pk=id, ).exists():
                        id = '%06d' % id
                        return redirect(to='admin_delivery:edit', id=id, )
                    else:
                        error_message = u'Рассылка с таким номером не существует.'
    #from datetime import datetime, timedelta
    #filter_datetime = datetime.now() - timedelta(days=93, )
    mailings = Delivery.objects.all()  # filter(created_at__gte=filter_datetime, )
    return render(request=request,
                  template_name=template_name,
                  context={'error_message': error_message,
                           'mailings': mailings, },
                  content_type='text/html', )


@staff_member_required
def add_edit(request,
             delivery_id=None,
             template_name=u'delivery/add_edit.jinja2', ):
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
            send_spam = request.POST.get(u'send_spam', None, )
            if send_spam == None:
                send_spam = True
            else:
                if isinstance(send_spam, unicode, ):
                    try:
                        send_spam = int(send_spam, )
                    except Exception as inst:
                        send_spam = True
                    else:
                        send_spam = bool(send_spam, )
                else:
                    send_spam = True
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
                    return redirect(to='admin_delivery:index', )

            delivery.name = name
            delivery.delivery_test = test
            delivery.send_test = send_test
            delivery.send_spam = send_spam
            delivery.send_general = send_general
            # print test
            delivery.type = delivery_type
            delivery.subject = subject
            delivery.html = html
            delivery.save()
            """ Обрабатываем картинки. """
            for i in range(1, 50):
                print i
                image_pk = 'image_pk_%d' % i
                image_pk = request.POST.get('image_pk_%d' % i, False, )
                if image_pk:
                    try:
                        image_pk = int(image_pk, )
                    except ValueError:
                        image_pk = 0
                    if image_pk != 0:
                        """ Редактируется ссылка на существующую картинку """
                        try:
                            image = Email_Img.objects.get(pk=image_pk, )
                        except Email_Img.DoesNotExist:
                            image = Email_Img()
                    else:
                        image = Email_Img()
                    image_name = request.POST.get('image_name_%d' % i, False, )
                    if image_name:
                        image.name = image_name
                    image_tag_name = request.POST.get('image_tag_name_%d' % i, False, )
                    if image_tag_name:
                        image.tag_name = image_tag_name
                    image_file = request.FILES.get('image_%d' % i, False, )
                    print image_file
                    image.parent = delivery
                    if image_file:
                        image.image = image_file
                        print '2'
                        image.save()
            return redirect(to='admin_delivery:index', )

    if delivery_id:
        try:
            delivery_id = int(delivery_id, )
        except ValueError:
            error_message = u'Некорректно введен номер рассылки.'
            return redirect(to='admin_delivery:index', )
        else:
            try:
                delivery = Delivery.objects.get(pk=delivery_id, )
            except Delivery.DoesNotExist:
                error_message = u'В базе отсутсвует рассылка с таким номером.'
                return redirect(to='admin_delivery:index', )
    else:
        delivery = None
    type_mailings = Delivery.Type_Mailings
    return render(request=request,
                  template_name=template_name,
                  context={'delivery_id': delivery_id,
                           'delivery': delivery,
                           'type_mailings': type_mailings,
                           'form': DeliveryCreateEditForm, },
                  content_type='text/html', )


@staff_member_required
def start_delivery(request,
                   delivery_id=None,
                   delivery_type='test', ):
    if request.method == "POST":
        POST_NAME = request.POST.get(u'POST_NAME', None, )

        if POST_NAME in ('start_delivery_test', 'start_delivery_general'):
            if delivery_id:
                try:
                    delivery_id = int(delivery_id, )
                except ValueError:
                    """ Уже РЕДИРЕКТ отсюда """
                    error_message = u'Отсутвует номер рассылки'
                    return redirect(to='admin_delivery:index', )
                else:
                    try:
                        delivery = Delivery.objects.get(pk=delivery_id, )
                    except Delivery.DoesNotExist:
                        error_message = u'В базе отсутсвует рассылка с таким номером.'
                        return redirect(to='admin_delivery:index', )

                    else:
                        if POST_NAME == 'start_delivery_test' \
                                and delivery_type == 'test' \
                                and not delivery.send_test:

                            pass
#                            call_command(name='processing_delivery_send_test',
#                                         delivery_pk=delivery_id,
#                                         delivery_test=True,
#                                         delivery_general=False, )

                        elif POST_NAME == 'start_delivery_general' \
                                and delivery_type == 'general' \
                                and delivery.send_test \
                                and not delivery.send_general:

                            call_command(name='processing_delivery_send',
                                         delivery_pk=delivery_id,
                                         delivery_test=False,
                                         delivery_general=True, )

                        processing_delivery.apply_async(
                            queue='celery',
                            kwargs={'delivery_type': delivery_type, 'delivery_pk': delivery.pk, }, )

    return redirect(to='admin_delivery:index', )


@staff_member_required
def exclude_email_from_delivery(request,
                                template_name=None, ):
    if request.method == "POST":
        POST_NAME = request.POST.get(u'POST_NAME', None, )
        if POST_NAME == 'exclude_email':
            email = request.POST.get(u'bad_email', None, )
            try:
                email = Email.objects.get(email=email, )
            except Email.DoesNotExist:
                error_message = u'В базе отсутсвует такой E-Mail.'
            else:
                email.bad_email = True
                email.save()
            try:
                email = SpamEmail.objects.get(email=email, )
            except SpamEmail.DoesNotExist:
                error_message = u'В базе отсутсвует такой E-Mail.'
            else:
                email.bad_email = True
                email.save()
    return redirect(to='admin_delivery:index', )
