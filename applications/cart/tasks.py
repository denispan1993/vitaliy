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

    if order.recompile:
        return order

    username, first_name, last_name, patronymic = processing_username(order=order, )

    logger.info('UserName123: %s' % username, )
    sessionID = order.sessionid
    logger.info('sessionID321: %s' % sessionID, )

    try:
        sessionID = Session_ID.objects.get(sessionid=sessionID, )
        if sessionID.user:
            user = sessionID.user
    except Session_ID.DoesNotExist:
        pass

    if 'user' not in (locals(), globals()):
        if order.email:
            email = order.email.replace(' ', '', )
            logger.info('E-Mail1: 123 | %s' % email, )
        else:
            email = None
    else:
        # email = user.email_parent_user.get()
        # print 'E-Mail 2.1: ', email
        email = user.email_parent_user.all()
        logger.info('E-Mail 2.2: 324 | %s' % email, )
        if not email:  # == []:
            user.delete()
        else:
            email = user.email_parent_user.all()[0]
            logger.info('E-Mail 2.3: 2432 | %s' % email.email, )

    if type(email, ) != Email:
        try:
            email = Email.objects.get(email=email, )
        except Email.DoesNotExist:
            email_not_found = True
        except MySQLdb.Warning as e:
            logger.info('cart/tasks.py: | %s ' % e.args, )
            logger.info('cart/tasks.py: 654 | %s' % e.message, )
            e_message = e.message.split(' ')[2]
            logger.info('cart/tasks.py: 468 | %s' % e_message, )
            if e_message == 'DOUBLE':
                try:
                    emails = Email.objects.filter(email=email, )
                except:
                    pass
                logger.info('cart/tasks.py: 098: | %s' % emails, )
                logger.info('cart/tasks.py: 23122: | %s' % len(emails, ), )
                emails[0].delete()
                try:
                    email = Email.objects.get(email=email, )
                except:
                    pass
            logger.info('cart/tasks.py: 745: | %s' % e.__doc__, )
        else:
            if type(sessionID) != Session_ID:
                user = email.user
            else:
                if email.user == sessionID.user:
                    logger.info(u'Ok', u' - ', u'SessionID.user == Email.user')
                else:
                    logger.info(u'Хреново, Email и SessionID пренадлежат разным пользователям.', )
                    logger.info(u'SessionID.user: | %s' % sessionID.user, )
                    logger.info(u'Email.user: | %s' % email.user, )

    phone = r'%s' % order.phone
    phone = phone\
        .replace(' ', '', ).replace('(', '', ).replace(')', '', )\
        .replace('-', '', ).replace('.', '', ).replace(',', '', )\
        .replace('/', '', ).replace('|', '', ).replace('\\', '', )\
        .lstrip('+380').lstrip('380').lstrip('38').lstrip('80').lstrip('0')
    logger.info('phone: ', phone, )

    try:
        int_phone_code = int(phone[:2])
        int_phone = int(phone[2:])
    except ValueError:
        int_phone_code = 0
        int_phone = 0

    try:
        phone = Phone.objects.get(
            phone='{phone_code}{phone}'.format(
                phone_code=str(int_phone_code, ),
                phone='{int_phone:07d}'.format(int_phone=int_phone, ),
            ),
        )
    except Phone.DoesNotExist:
        phone_not_found = True
    except Phone.MultipleObjectsReturned:
        phones = Phone.objects.filter(
            phone='{phone_code}{phone}'.format(
                phone_code=str(int_phone_code, ),
                phone='{int_phone:07d}'.format(int_phone=int_phone, ),
            ),
        )

        logger.info('%d' % len(phones, ), )
        if len(phones, ) > 1:
            phones[0].delete()
            phone = phones[1]
    else:
        if type(sessionID) != Session_ID and type(email) != Email:
            user = phone.user
        else:
            if ('user' in locals() or 'user' in globals()) and user == phone.user:
                logger.info(u'Phone.user == User', )
            else:
                logger.info(u'Номер телефона зарегистрирован за другим пользователем', )
                if type(sessionID) == Session_ID:
                    logger.info(u'SessionID.user: %s' % sessionID.user, )
                if type(email) == Email:
                    logger.info(u'Email.user: %s' % email.user, )
                logger.info(u'Phone.user: %s' % phone.user, )

    if 'user' not in locals() and 'user' not in globals():
        try:
            user = User.objects.get(username=username, )
        except User.DoesNotExist:
            user = User.objects.create(username=username,
                                       first_name=first_name,
                                       last_name=last_name,
                                       patronymic=patronymic,
                                       last_login=timezone.now(), )

    if type(sessionID) != Session_ID:
        sessionID = Session_ID.objects.create(user=user, sessionid=sessionID, )
    else:
        sessionID.user = user
        sessionID.save()

    if isinstance(email, str) or not email:  # type(email, ) == 'unicode':
        logger.info('email type: %s email: %s' % (type(email, ), email, ), )
    else:
        logger.info('email type: %s email: %s' % (type(email, ), email.email, ), )

    if email is not None:
        if type(email) != Email:
            email = Email.objects.create(user=user, email=email, )
        else:
            email.user = user
            email.save()

    if type(phone) != Phone:
        #if 'phone1' in locals() or 'phone1' in globals() and 'phone2' in locals() or 'phone2' in globals():
        #    Phone.objects.create(user=user, phone=phone1, )
        #    del phone1
        #    Phone.objects.create(user=user, phone=phone2, )
        #    del phone2
        #else:
        Phone.objects.create(user=user, phone=phone, int_phone=int_phone, int_phone_code=int_phone_code, )
    else:
        phone.user = user
        phone.save()

    order.user = user
    order.recompile = True
    order.save()

    stop = datetime.now()
    logger.info(u'Stop: generate_prom_ua_yml(*args, **kwargs): datetime.now() {0} | {1}'.format(stop, (stop - start), ), )

    return order


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
