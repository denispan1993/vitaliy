# -*- coding: utf-8 -*-

from proj.celery import celery_app
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.core.mail.backends import smtp
from django.utils.html import strip_tags
from time import sleep

import email

from .models import Order

__author__ = 'AlexStarov'


@celery_app.task()
def delivery_order(*args, **kwargs):

    order_pk = int(kwargs.get('order_pk'))

    try:
        order = Order.objects.get(pk=order_pk)
    except Order.DoesNotExist:
        return False

    """ Отправка заказа мэнеджеру """
    html_content = render_to_string('email_order_content.jinja2',
                                    {'order': order, })

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
#        ssl_certfile=None,
#        **kwargs)
    backend = smtp.EmailBackend(
        host='smtp.yandex.ru',
        port=465,
        username='site@keksik.com.ua',
        password='1q2w3e4r',
        use_tls=False,
        fail_silently=False,
        use_ssl=True,
        timeout=30,
        ssl_keyfile=None,
        ssl_certfile=None,
        **kwargs)

    msg = EmailMultiAlternatives(
        subject=u'Заказ № %d. Кексик.' % order.pk,
        body=strip_tags(html_content, ),
        from_email=email.utils.formataddr((u'Интернет магазин Keksik', u'site@keksik.com.ua')),
        to=[email.utils.formataddr((u'Email zakaz@ Интернет магазин Keksik', u'zakaz@keksik.com.ua')), ],
        connection=backend, )

    msg.attach_alternative(content=html_content,
                           mimetype="text/html", )

    msg.content_subtype = "html"
    i = 0
    while True:
        result = msg.send(fail_silently=False, )

        if (isinstance(result, int) and result == 1) or i > 100:
            i = 0
            break

        print('cart.tasks.delivery_order.admin(i): ', i, ' result: ', result, )
        i += 1
        sleep(5)

    """ Отправка благодарности клиенту. """
    html_content = render_to_string('email_successful_content.jinja2',
                                    {'order': order, })
    msg = EmailMultiAlternatives(
        subject=u'Заказ № %d. Интернет магазин Кексик.' % order.pk,
        body=strip_tags(html_content, ),
        from_email=email.utils.formataddr((u'Интернет магазин Keksik', u'zakaz@keksik.com.ua')),
        to=[email.utils.formataddr((order.FIO, order.email)), ],
        connection=backend, )

    msg.attach_alternative(content=html_content,
                           mimetype="text/html", )

    while True:
        result = msg.send(fail_silently=False, )

        if (isinstance(result, int) and result == 1) or i > 100:
            break

        print('cart.tasks.delivery_order.user(i): ', i, ' result: ', result, )
        i += 1
        sleep(5)

    return True


def aaa():
    """ YowSup2 - Gateway """

    from yowsup_gateway import YowsupGateway

    gateway = YowsupGateway(credentials=("380664761290", "rw/XJQWbcCDpcDjpZ7BL8RItdQo="))

    result = gateway.send_messages([("380952886976", "Номер Вашего заказа %d\nВаш магазин Кексик." % order.pk)])
    if result.is_success:
        print result.inbox, result.outbox

    # Receive messages
    result = gateway.receive_messages()
    if result.is_sucess:
        print result.inbox, result.outbox
