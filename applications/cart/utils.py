# -*- coding: utf-8 -*-
# /apps/cart/utils.py

import MySQLdb
import smtplib
import email
from time import sleep

from django.template import Context, Template
from django.template.loader import render_to_string
from django.core.mail.backends import smtp
from django.contrib.auth import get_user_model

from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags

from pytils.translit import slugify
from celery.utils.log import get_task_logger

from applications.delivery2.models import EmailTemplate
from applications.authModel.models import Email, Phone

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


def get_and_render_template(template_name, **kwargs):
    try:
        template = EmailTemplate.objects.get(name=template_name, )
        html_content = template.get_template()
        t = Template(html_content)
        c = Context(kwargs)
        return t.render(c)
    except EmailTemplate.DoesNotExist:
        return None


def send_email(subject='Спасибо за заказ в магазине Кексик',
               from_email=email.utils.formataddr((u'Интернет магазин Keksik', u'site@keksik.com.ua')),
               to_emails=[email.utils.formataddr((u'Email zakaz@ Интернет магазин Keksik', u'zakaz@keksik.com.ua')), ],
               html_content=None,
               ext_backend=None, ):

    msg = EmailMultiAlternatives(
        subject=subject,  # 'Заказ № %d. Кексик.' % order.number,
        from_email=from_email,
        to=to_emails,
        body=strip_tags(html_content, ),
        connection=ext_backend if ext_backend else backend, )

    msg.attach_alternative(content=html_content,
                           mimetype="text/html", )

    msg.content_subtype = "html"
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

    from .models import Cart
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


def get_email(order, ):

    email = order.email.replace(' ', '', )
    logger.info('get_email: email: %s' % email, )

    try:
        return Email.objects.get(email=email, )

    except Email.DoesNotExist:
        return Email.objects.create(email=email, )

    except MySQLdb.Warning as e:
        logger.info('cart/tasks.py/get_email/e.args: %s' % e.args, )
        logger.info('cart/tasks.py/get_email/e.message: %s' % e.message, )
        logger.info('cart/tasks.py/get_email/__doc__: %s' % e.__doc__, )
        e_message = e.message.split(' ')[2]
        logger.info('cart/tasks.py/get_email/e_message/split: 468 | %s' % e_message, )

        if e_message == 'DOUBLE':
            emails = Email.objects.filter(email=email, )
            logger.info('cart/tasks.py/get_email/DOUBLE: len(): %d | %s' % (len(emails, ), emails, ), )
            emails[0].delete()
            try:
                return Email.objects.get(email=email, )
            except Email.DoesNotExist:
                return None


def get_phone(order, ):
    phone = r'%s'\
        .replace(' ', '', ).replace('(', '', ).replace(')', '', )\
        .replace('-', '', ).replace('.', '', ).replace(',', '', )\
        .replace('/', '', ).replace('|', '', ).replace('\\', '', )\
        .lstrip('+380').lstrip('380').lstrip('38').lstrip('80').lstrip('0')\
            % order.phone

    logger.info('get_phone: phone: %s' % phone, )

    try:
        int_code = int(phone[:2])
        int_phone = int(phone[2:])
    except ValueError:
        int_code = 0
        int_phone = 0

    try:
        return Phone.objects.get(
            phone='{phone_code}{phone}'.format(
                phone_code=str(int_code, ),
                phone='{int_phone:07d}'.format(int_phone=int_phone, ),
            ),
        )
    except Phone.DoesNotExist:
        return Phone.objects.create(phone=phone, int_phone=int_phone, int_code=int_code, )
    except Phone.MultipleObjectsReturned:
        phones = Phone.objects.filter(
            phone='{phone_code}{phone}'.format(
                phone_code=str(int_code, ),
                phone='{int_phone:07d}'.format(int_phone=int_phone, ),
            ),
        )

        logger.info('cart/tasks.py/get_phone/DOUBLE: len(): %d | %s' % (len(phones, ), phones,), )
        phones[0].delete()
        try:
            return Phone.objects.get(
                    phone='{phone_code}{phone}'.format(
                        phone_code=str(int_code, ),
                        phone='{int_phone:07d}'.format(int_phone=int_phone, ), ),
            )

        except Phone.DoesNotExist:
            return None


def processing_username(order, ):
    if '.' in order.FIO:
        FIO = order.FIO.split('.')
        FIO_temp = FIO
        if FIO[0][-1] == '.' and FIO[0][-3] == '.' \
                or 'Діденко' in FIO[0] \
                or 'Коба' in FIO[0] \
                or 'Слободянюк' in FIO[0] \
                or 'Корягина' in FIO[0] \
                or 'Дуянова' in FIO[0] \
                or 'Тарасова' in FIO[0] \
                or 'Пашпадурова' in FIO[0] \
                or 'Розкошинская' in FIO[0]:
            FIO = FIO[0].split()
            FIO[2] = FIO_temp[1]
        elif FIO[0][-1].isupper() and FIO[0][-2].isupper():
            FIO[0] = FIO_temp[:-2]
            FIO[1] = FIO_temp[-2]
            FIO[2] = FIO_temp[-1]
    else:
        FIO = order.FIO.split(' ')

    if len(FIO) == 3:
        last_name, first_name, patronymic = FIO
    elif len(FIO) == 2:
        last_name, first_name = FIO
        patronymic = u'Отчество'
    elif len(FIO) == 1:
        last_name = FIO
        first_name = u'Имя'
        patronymic = u'Отчество'
    else:
        last_name = u'Фамилия'
        first_name = u'Имя'
        patronymic = u'Отчество'

    if last_name:
        logger.info('Order.Pk: %d last_name: %s type: %s' % (order.pk, last_name, type(last_name), ), )
        if type(last_name, ) == list:
            last_name = last_name[0]  # .encode('UTF8', ),
        logger.info('Order.Pk: %d last_name: %s type: %s' % (order.pk, last_name, type(last_name), ), )
        last_name = last_name.lstrip('.')
        if len(last_name, ) > 30:
            logger.info('Order.Pk: %d last_name: %s type: %s' % (order.pk, last_name, type(last_name),), )
            last_name = last_name[:30]

    if first_name:
        logger.info('Order.Pk: %d first_name: %s type: %s' % (order.pk, first_name, type(first_name), ), )
        if type(first_name, ) == list:
            first_name = first_name
        logger.info('Order.Pk: %d first_name: %s type: %s' % (order.pk, first_name, type(first_name), ), )
        first_name = first_name.lstrip('.')
        if len(first_name, ) > 30:
            logger.info('Order.Pk: %d first_name: %s type: %s' % (order.pk, first_name, type(first_name),), )
            first_name = first_name[:30]

    if patronymic:
        logger.info('Order.Pk: %d patronymic: %s type: %s' % (order.pk, patronymic, type(patronymic), ), )
        if type(patronymic, ) == list:
            patronymic = patronymic
        logger.info('Order.Pk: %d patronymic: %s type: %s' % (order.pk, patronymic, type(patronymic), ), )
        patronymic = patronymic.lstrip('.')
        if len(patronymic, ) > 32:
            logger.info('Order.Pk: %d patronymic: %s type: %s' % (order.pk, patronymic, type(patronymic),), )
            patronymic = patronymic[:32]
        logger.info('Order.Pk: %d patronymic: %s type: %s' % (order.pk, patronymic, type(patronymic), ), )

    username = ''.join(['%s' % slugify(k).capitalize() for k in (last_name, first_name, patronymic)], )
    logger.info('Order.Pk: %d username: %s type: %s' % (order.pk, username, type(username),), )

    if type(username, ) == list:
        username = str(username, )
    logger.info('Order.Pk: %d username: %s type: %s' % (order.pk, username, type(username),), )

    if len(username, ) > 32:
        logger.info('Order.Pk: %d username: %s type: %s' % (order.pk, username, type(username),), )
        username = username[:32]

    return username, first_name, last_name, patronymic


def aaa():
    """ YowSup2 - Gateway """

    from yowsup_gateway import YowsupGateway

    gateway = YowsupGateway(credentials=("380664761290", "rw/XJQWbcCDpcDjpZ7BL8RItdQo="))

    result = gateway.send_messages([("380952886976", "Номер Вашего заказа %d\nВаш магазин Кексик." % order.pk)])
    if result.is_success:
        logger.info(result.inbox, result.outbox, )

    # Receive messages
    result = gateway.receive_messages()
    if result.is_sucess:
        logger.info(result.inbox, result.outbox, )
