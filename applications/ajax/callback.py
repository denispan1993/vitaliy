# -*- coding: utf-8 -*-
__author__ = 'Alex Starov'

try:
    from django.utils.simplejson import dumps
    # import simplejson as json
except ImportError:
    from json import dumps
    # import json

from django.http import HttpResponse


def callback_data_send(request, ):
    if request.is_ajax():
        if request.method == 'POST':
            # request_cookie = request.session.get(u'cookie', None, )
            # if request_cookie:
            sessionid = request.POST.get(u'sessionid', None, )
            print('CallBack:', )
            print('sessionid: ', sessionid, )
            userid = request.POST.get(u'userid', False, )
            print('userid: ', userid, )
            print('userid type: ', type(userid, ), )
            if userid == 'None':
                userid = False
            name = request.POST.get(u'name', None, )
            print('name: ', name.encode('utf8', ), )
            email = request.POST.get(u'email', None, )
            print('email: ', email, )
            phone = request.POST.get(u'phone', None, )
            print('phone: ', phone, )
            from applications.callback.models import CallBack
            try:
                if userid:
                    """ Error: invalid literal for int() with base 10: 'None' """
                    """ Ошибка вылазила из за того, что я пытался подсунуть вместо int() в user_id - None """
                    print(userid, )
                    callback = CallBack.objects.create(sessionid=sessionid,
                                                       user_id=userid,
                                                       name=name,
                                                       email=email,
                                                       phone=phone, )
                else:
                    callback = CallBack.objects.create(sessionid=sessionid,
                                                       name=name,
                                                       email=email,
                                                       phone=phone, )
            except Exception as e:
                print('Exception: ', e, )
                print('Exception message: ', e.message, )
                response = {'result': 'Bad',
                            'error': e.message, }
                data = dumps(response, )
                mimetype = 'application/javascript'
                return HttpResponse(data, mimetype, )
            else:
                print(callback, )
                """ Отправка заказа обратного звонка """
                subject = u'Заказ обратного звонка от пользователя: %s на номер: %s. Интернет магазин Кексик.' % (name, phone, )
                from django.template.loader import render_to_string
                html_content = render_to_string('email_request_callback_content.html',
                                                {'name': name,
                                                 'email': email,
                                                 'phone': phone, }, )
                from django.utils.html import strip_tags
                text_content = strip_tags(html_content, )
                from_email = u'Интерент магазин Кексик <site@keksik.com.ua>'
                from django.core.mail import get_connection
                backend = get_connection(backend='django.core.mail.backends.smtp.EmailBackend',
                                         fail_silently=False, )
                from django.core.mail import EmailMultiAlternatives
                from proj.settings import Email_MANAGER
                msg = EmailMultiAlternatives(subject=subject,
                                             body=text_content,
                                             from_email=from_email,
                                             to=[Email_MANAGER, ],
                                             connection=backend, )
                msg.attach_alternative(content=html_content,
                                       mimetype="text/html", )
                msg.content_subtype = "html"
                msg.send(fail_silently=False, )
                """ Отправка благодарности клиенту. """
                subject = u'Ваш заказ обратного звонка с сайта принят. Интернет магазин Кексик.'
                html_content = render_to_string('email_successful_request_callback_content.html', )
                text_content = strip_tags(html_content, )
                # from_email = u'site@keksik.com.ua'
                to_email = email
                msg = EmailMultiAlternatives(subject=subject,
                                             body=text_content,
                                             from_email=from_email,
                                             to=[to_email, ],
                                             connection=backend, )
                msg.attach_alternative(content=html_content,
                                       mimetype="text/html", )
                from smtplib import SMTPSenderRefused, SMTPDataError
                try:
                    msg.send(fail_silently=False, )
                except SMTPSenderRefused as e:
                    response = {'result': 'Bad',
                                'error': e, }
                else:
                    response = {'result': 'Ok', }
                data = dumps(response, )
                mimetype = 'application/javascript'
                return HttpResponse(data, mimetype, )
            # else:
            #     response = {'result': 'Bad',
            #                 'error': u'Вы только-что зашли на сайт!!!', }
            #     data = dumps(response, )
            #     mimetype = 'application/javascript'
            #     return HttpResponse(data, mimetype, )
        elif request.method == 'GET':
            return HttpResponse(status=400, )
        else:
            return HttpResponse(status=400, )
    else:
        return HttpResponse(status=400, )
