# -*- coding: utf-8 -*-
__author__ = 'Alex Starov'

try:
    from django.utils.simplejson import dumps
    # import simplejson as json
except ImportError:
    from json import dumps
    # import json

from django.http import HttpResponse


def feedback_data_send(request, ):
    if request.is_ajax():
        if request.method == 'POST':
            request_cookie = request.session.get(u'cookie', None, )
            if request_cookie:
                sessionid = request.POST.get(u'sessionid', None, )
                user_id = request.POST.get(u'user_id', None, )
                from django.contrib.auth import get_user_model
                UserModel = get_user_model()
                if user_id and request.user.is_authenticated() and request.user.is_active:
                    user_id = request.session.get(u'_auth_user_id', None, )
                    # from django.contrib.auth.models import User
                    try:
                        user_id = int(user_id, )
                    except ValueError:
                        user_id = -1
                else:
                    user_id = -1

                name = request.POST.get(u'name', None, )
                email = request.POST.get(u'email', None, )
                phone = request.POST.get(u'phone', None, )
                comment = request.POST.get(u'comment', None, )
                from apps.comment.models import Comment
                try:
                    Comment.objects.create(sessionid=sessionid,
                                           user_id=user_id,
                                           name=name,
                                           email_for_response=email,
                                           phone=phone,
                                           comment=comment, )
                except Exception as e:
                    if e.message is None:
                        response = {'result': 'Bad',
                                    'exception': e, }
                    else:
                        response = {'result': 'Bad',
                                    'error': e.message,
                                    'exception': e, }
                    data = dumps(response, )
                    mimetype = 'application/javascript'
                    return HttpResponse(data, mimetype, )
                else:
                    """ Отправка жалобы/комментария """
                    subject = u'Жалоба/комментарий от пользователя: %s.' % name
                    from django.template.loader import render_to_string
                    html_content = render_to_string('email_feedback_content.html',
                                                    {'name': name,
                                                     'email': email,
                                                     'phone': phone,
                                                     'comment': comment, }, )
                    from django.utils.html import strip_tags
                    text_content = strip_tags(html_content, )
                    from_email = u'site@keksik.com.ua'
                    from django.core.mail import get_connection
                    backend = get_connection(backend='django.core.mail.backends.smtp.EmailBackend',
                                             fail_silently=False, )
                    from django.core.mail import EmailMultiAlternatives
                    from proj.settings import Email_MANAGER
                    msg = EmailMultiAlternatives(subject=subject,
                                                 body=text_content,
                                                 from_email=from_email,
                                                 to=['lana24680@keksik.com.ua', ],
                                                 connection=backend, )
                    msg.attach_alternative(content=html_content,
                                           mimetype="text/html", )
                    msg.content_subtype = "html"
                    msg.send(fail_silently=False, )
                    """ Отправка благодарности клиенту. """
                    subject = u'Ваша жалоба/комментарий принят. Интернет магазин Кексик.'
                    html_content = render_to_string('email_successful_feedback_content.html', )
                    text_content = strip_tags(html_content, )
                    from_email = u'site@keksik.com.ua'
                    msg = EmailMultiAlternatives(subject=subject,
                                                 body=text_content,
                                                 from_email=from_email,
                                                 to=[email, ],
                                                 connection=backend, )
                    msg.attach_alternative(content=html_content,
                                           mimetype="text/html", )
                    from smtplib import SMTPRecipientsRefused
                    try:
                        msg.send(fail_silently=False, )
                    except SMTPRecipientsRefused:
                        response = {'result': 'Bad',
                                    'error': u'Почтовый сервер не принял E-Mail адерс получателя'}
                    else:
                        response = {'result': 'Ok', }
                    data = dumps(response, )
                    mimetype = 'application/javascript'
                    return HttpResponse(data, mimetype, )
            else:
                response = {'result': 'Bad',
                            'error': u'Вы только-что зашли на сайт!!!', }
                data = dumps(response, )
                mimetype = 'application/javascript'
                return HttpResponse(data, mimetype, )
        elif request.method == 'GET':
            return HttpResponse(status=400, )
        else:
            return HttpResponse(status=400, )
    else:
        return HttpResponse(status=400, )
