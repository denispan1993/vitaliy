# -*- coding: utf-8 -*-
# /apps/cart/utils.py

import smtplib
import email
from time import sleep

from django.template import Context, Template
from django.template.loader import render_to_string
from django.core.mail.backends import smtp
from django.contrib.auth import get_user_model

from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags

from celery.utils.log import get_task_logger

from applications.delivery2.models import EmailTemplate
from .models import Cart

__author__ = 'AlexStarov'


logger = get_task_logger(__name__)


#    backend = smtp.EmailBackend(
#        host='192.168.1.95',
#        port=465,
#        username='delivery@keksik.com.ua',
#        password='warning123',
#        use_tls=False,
#        fail_silently=False,
#        use_ssl=True,
#        timeout=30,
#        ssl_keyfile=None,
#        ssl_certfile=None, )
backend = smtp.EmailBackend(
    host='smtp.yandex.ru',
    port=465,
    username='site@keksik.com.ua',
    password='1q2w3e4r!!!@@@',
    use_tls=False,
    fail_silently=False,
    use_ssl=True,
    timeout=30,
    ssl_keyfile=None,
    ssl_certfile=None, )


def get_and_render_template(order, template_name, ):
    try:
        template = EmailTemplate.objects.get(name=template_name, )
        html_content = template.get_template()
        t = Template(html_content)
        c = Context({'order': order, })
        return t.render(c)
    except EmailTemplate.DoesNotExist:
        return None


def send_email(subject='Спасибо за заказ в магазине Кексик',
               from_email=email.utils.formataddr((u'Интернет магазин Keksik', u'site@keksik.com.ua')),
               to_emails=[email.utils.formataddr((u'Email zakaz@ Интернет магазин Keksik', u'zakaz@keksik.com.ua')), ],
               html_content=None):

    msg = EmailMultiAlternatives(
        subject=subject,  # 'Заказ № %d. Кексик.' % order.number,
        from_email=from_email,
        to=to_emails,
        body=strip_tags(html_content, ),
        connection=backend, )

    msg.attach_alternative(content=html_content,
                           mimetype="text/html", )

    # msg.content_subtype = "html"
    i = 0
    while True:

        try:
            result = msg.send(fail_silently=False, )
        except smtplib.SMTPDataError as e:
            result = False
            logger.info('print e: cart/task.py: ', e, )

        if (isinstance(result, int) and result == 1) or i > 100:
            i = 0
            break

        logger.info('cart.tasks.delivery_order.admin(i)(utils): ', i, ' result: ', result, )
        i += 1
        sleep(15)


def get_cart_or_create(request, user_object=False, created=True, ):
    sessionid = request.COOKIES.get(u'sessionid', None, )

    if not user_object:
        if request.user.is_authenticated() and request.user.is_active:
            user_id_ = request.session.get(u'_auth_user_id', None, )

            try:
                user_id_ = int(user_id_, )
                user_object = get_user_model().objects.get(pk=user_id_, )
            except ValueError:
                user_object = None
        else:
            user_object = None

    if created:
        cart, created = Cart.objects.get_or_create(user=user_object,
                                                   sessionid=sessionid, )
    else:
        try:
            cart = Cart.objects.get(user=user_object,
                                    sessionid=sessionid, )
        except Cart.DoesNotExist:
            cart = None
        return cart

    return cart, created
