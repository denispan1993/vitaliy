# -*- coding: utf-8 -*-
import MySQLdb
from datetime import datetime
import email
from django.template.loader import render_to_string
from proj.celery import celery_app
from django.utils import timezone
from pytils.translit import slugify
from celery.utils.log import get_task_logger


import proj.settings

from applications.account.models import Session_ID
from applications.authModel.models import User, Email, Phone
from .utils import get_and_render_template, send_email

__author__ = 'AlexStarov'

logger = get_task_logger(__name__)


@celery_app.task()
def delivery_order(*args, **kwargs):

    from .models import Order
    try:
        order = Order.objects.get(pk=kwargs.get('order_pk'))
    except Order.DoesNotExist:
        return False

    """ Отправка заказа мэнеджеру """
    template_name = kwargs.pop('email_template_name_to_admin',
                               proj.settings.EMAIL_TEMPLATE_NAME['SEND_ORDER_TO_ADMIN'], )
    html_content = get_and_render_template(order=order, template_name=template_name)

    if not html_content:
        html_content = render_to_string('email_order_content.jinja2',
                                        {'order': order, })

    send_email(subject='Заказ № %d. Кексик.' % order.number,
               from_email=email.utils.formataddr((u'Интернет магазин Keksik', u'site@keksik.com.ua')),
               to_emails=[email.utils.formataddr((u'Email zakaz@ Интернет магазин Keksik', u'zakaz@keksik.com.ua')), ],
               html_content=html_content, )

    """ Отправка благодарности клиенту. """
    logger.info('order.email: ', order.email,
          ' bool: ', order.email is 'alex.starov@keksik.com.ua',
          ' bool: ', 'keksik.com.ua' in order.email,
          ' email: ', 'alex.starov@keksik.com.ua')

    template_name = kwargs.pop('email_template_name_to_client',
                               proj.settings.EMAIL_TEMPLATE_NAME['SEND_ORDER_NUMBER'], )

    logger.info('template_name: ', template_name, )

    html_content = get_and_render_template(order=order, template_name=template_name)

    if not html_content:
        html_content = render_to_string('email_successful_content.jinja2',
                                        {'order': order, })

    logger.info('html_content: ', html_content)

    send_email(
        subject=u'Заказ № %d. Интернет магазин Кексик.' % order.number,
        from_email=email.utils.formataddr((u'Интернет магазин Keksik', u'site@keksik.com.ua')),
        to_emails=[email.utils.formataddr((order.FIO, order.email)), ],
        html_content=html_content, )

    return True


@celery_app.task()
def recompile_order(*args, **kwargs):

    start = datetime.now()
    logger.info(u'Start: recompile_order(*args, **kwargs): datetime.now() {0}'.format(start), )

    order_pk = int(kwargs.get('order_pk'))

    from .models import Order
    try:
        order = Order.objects.get(pk=order_pk)
    except Order.DoesNotExist:
        return False

    #if order.recompile:
    #    return order

    username, first_name, last_name, patronymic = processing_username(order=order, )
    """ Сначала ищем пользователя по username """
    try:
        user = User.objects.get(username=username, )
    except User.DoesNotExist:
        user = None
    """ Теперь ищем юзера по email """
    email = get_email(order=order, )
    if email is not None and user is None:
        user = email.user if email.user else None
    """ Затем ищем юзера по номеру телефона """
    phone = get_phone(order=order, )
    if phone is not None and user is None:
        user = phone.user if phone.user is None else None
    """ Может мы его найдем по sessionID ? """
    sessionID = order.sessionid
    logger.info('cart/task.py/recompile_order: username -> %s | sessionID -> %s' % (username, sessionID, ), )

    try:
        sessionID = Session_ID.objects.get(sessionid=sessionID, )
    except Session_ID.DoesNotExist:
        sessionID = Session_ID.objects.create(sessionid=sessionID, )

    if user is None and sessionID is not None:
        user = sessionID.user if sessionID.user is not None else None

    """ Если все совсем плохо и мы не можем найти пользователя, то создаем его "нового" """
    if user is None:
        user = User.objects.create(username=username,
                                   first_name=first_name,
                                   last_name=last_name,
                                   patronymic=patronymic,
                                   last_login=timezone.now(), )

    """ Не отвязываем email и номер телефона от "Прежнего" пользователя
        если он есть !?!?!? """
    if email is not None and email.user is None:
        email.user = user
        email.save()

    elif email is not None and email.user is not None and email.user is not user:
        """ Пользователь user и email.user не совпадают !!! """
        logger.info('cart/task.py/recompile_order: email.user -> %s | user -> %s' % (email.user, user, ), )

    elif email is not None and email.user is user:
        """ Все OK. User и email.user совпали, как и должно было быть !!! """
        pass

    if phone is not None and phone.user is None:
        phone.user = user
        phone.save()

    elif phone is not None and phone.user is not None and phone.user is not user:
        """ Пользователь user и phone.user не совпадают !!! """
        logger.info('cart/task.py/recompile_order: phone.user -> %s | user -> %s' % (phone.user, user, ), )

    elif phone is not None and phone.user is user:
        """ Все OK. User и phone.user совпали, как и должно было быть !!! """
        pass

    if sessionID.user is None:
        sessionID.user = user
        sessionID.save()

    order.user = user
    order.recompile = True
    order.save()

    stop = datetime.now()
    logger.info(u'Stop: recompile_order(*args, **kwargs): datetime.now() {0} | {1}'.format(stop, (stop - start), ), )

    return user


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
                or 'Діденко'.decode('utf-8') in FIO[0] \
                or 'Коба'.decode('utf-8') in FIO[0] \
                or 'Слободянюк'.decode('utf-8') in FIO[0] \
                or 'Корягина'.decode('utf-8') in FIO[0] \
                or 'Дуянова'.decode('utf-8') in FIO[0] \
                or 'Тарасова'.decode('utf-8') in FIO[0] \
                or 'Пашпадурова'.decode('utf-8') in FIO[0] \
                or 'Розкошинская'.decode('utf-8') in FIO[0]:
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
