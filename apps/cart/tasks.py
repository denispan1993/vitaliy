# -*- coding: utf-8 -*-
import MySQLdb
from time import sleep
import smtplib
import email
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.core.mail.backends import smtp
from django.utils.html import strip_tags
from proj.celery import celery_app
from django.utils import timezone
from pytils.translit import slugify

import proj.settings

from apps.delivery2.models import EmailTemplate
from apps.account.models import Session_ID
from apps.authModel.models import User, Email, Phone

__author__ = 'AlexStarov'


@celery_app.task(name='celery_task_delivery_order')
def delivery_order(*args, **kwargs):

    order_pk = int(kwargs.get('order_pk'))

    from .models import Order
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
        password='1q2w3e4r!!!@@@',
        use_tls=False,
        fail_silently=False,
        use_ssl=True,
        timeout=30,
        ssl_keyfile=None,
        ssl_certfile=None,
        **kwargs)

    msg = EmailMultiAlternatives(
        subject=u'Заказ № %d. Кексик.' % order.number,
        body=strip_tags(html_content, ),
        from_email=email.utils.formataddr((u'Интернет магазин Keksik', u'site@keksik.com.ua')),
        to=[email.utils.formataddr((u'Email zakaz@ Интернет магазин Keksik', u'zakaz@keksik.com.ua')), ],
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
            print e

        if (isinstance(result, int) and result == 1) or i > 100:
            i = 0
            break

        print('cart.tasks.delivery_order.admin(i): ', i, ' result: ', result, )
        i += 1
        sleep(15)

    """ Отправка благодарности клиенту. """
    if order.email is 'alex.starov@keksik.com.ua':

        # proj.settings.EMAIL_TEMPLATE_NAME['SEND_ORDER_NUMBER']

        template_name = kwargs.pop('email_template_name', False, )

        try:
            template = EmailTemplate.objects.get(name=template_name, )
            html_content = template.get_template()

        except EmailTemplate.DoesNotExist:
            html_content = render_to_string('email_successful_content.jinja2',
                                            {'order': order, })

    else:

        html_content = render_to_string('email_successful_content.jinja2',
                                        {'order': order, })


    msg = EmailMultiAlternatives(
        subject=u'Заказ № %d. Интернет магазин Кексик.' % order.number,
        body=strip_tags(html_content, ),
        from_email=email.utils.formataddr((u'Интернет магазин Keksik', u'site@keksik.com.ua')),
        to=[email.utils.formataddr((order.FIO, order.email)), ],
        connection=backend, )

    msg.attach_alternative(content=html_content,
                           mimetype="text/html", )

    i = 0
    while True:

        try:
            result = msg.send(fail_silently=False, )
        except smtplib.SMTPDataError as e:
            result = False
            print e

        if (isinstance(result, int) and result == 1) or i > 100:
            break

        print('cart.tasks.delivery_order.user(i): ', i, ' result: ', result, )
        i += 1
        sleep(15)

    return True


@celery_app.task(name='celery_task_recompile_order')
def recompile_order(*args, **kwargs):

    order_pk = int(kwargs.get('order_pk'))

    from .models import Order
    try:
        order = Order.objects.get(pk=order_pk)
    except Order.DoesNotExist:
        return False

    if order.recompile:
        return order

    username, first_name, last_name, patronymic = processing_username(order=order, )

    print 'UserName: ', username
    sessionID = order.sessionid
    print sessionID

    try:
        sessionID = Session_ID.objects.get(sessionid=sessionID, )
        if sessionID.user:
            user = sessionID.user
    except Session_ID.DoesNotExist:
        pass

    if 'user' not in (locals(), globals()):
        if order.email:
            email = order.email.replace(' ', '', )
            print 'E-Mail1: ', email
        else:
            email = None
    else:
        # email = user.email_parent_user.get()
        # print 'E-Mail 2.1: ', email
        email = user.email_parent_user.all()
        print 'E-Mail 2.2: ', email
        if not email:  # == []:
            user.delete()
        else:
            email = user.email_parent_user.all()[0]
            print 'E-Mail 2.3: ', email.email

    if type(email, ) != Email:
        try:
            email = Email.objects.get(email=email, )
        except Email.DoesNotExist:
            email_not_found = True
        except MySQLdb.Warning, e:
            print e.args
            print e.message
            e_message = e.message.split(' ')[2]
            print e_message
            if e_message == 'DOUBLE':
                try:
                    emails = Email.objects.filter(email=email, )
                except:
                    pass
                print emails
                print len(emails, )
                emails[0].delete()
                try:
                    email = Email.objects.get(email=email, )
                except:
                    pass
            print e.__doc__
        else:
            if type(sessionID) != Session_ID:
                user = email.user
            else:
                if email.user == sessionID.user:
                    print u'Ok', u' - ', u'SessionID.user == Email.user'
                else:
                    print u'Хреново, Email и SessionID пренадлежат разным пользователям.'
                    print u'SessionID.user: ', sessionID.user
                    print u'Email.user: ', email.user

    phone = r'%s' % order.phone
    phone = phone\
        .replace(' ', '', ).replace('(', '', ).replace(')', '', )\
        .replace('-', '', ).replace('.', '', ).replace(',', '', )\
        .replace('/', '', ).replace('|', '', ).replace('\\', '', )\
        .lstrip('+380').lstrip('380').lstrip('38').lstrip('80').lstrip('0')
    print 'phone: ', phone

    try:
        int_phone_code = int(phone[:2])
        int_phone = int(phone[2:])
    except ValueError:
        pass

    try:
        phone = Phone.objects.get(
            phone='{phone_code}{phone}'\
                .format(
                    phone_code=str(int_phone_code, ),
                    phone='{int_phone:07d}'.format(int_phone=int_phone, ),
                ),
            )
    except Phone.DoesNotExist:
        phone_not_found = True
    except Phone.MultipleObjectsReturned:
        phones = Phone.objects.filter(
            phone='{phone_code}{phone}'
                .format(
                    phone_code=str(int_phone_code, ),
                    phone='{int_phone:07d}'.format(int_phone=int_phone, ),
                ),
        )

        print len(phones, )
        if len(phones, ) > 1:
            phones[0].delete()
            phone = phones[1]
    else:
        if type(sessionID) != Session_ID and type(email) != Email:
            user = phone.user
        else:
            if ('user' in locals() or 'user' in globals()) and user == phone.user:
                print u'Phone.user == User'
            else:
                print u'Номер телефона зарегистрирован за другим пользователем'
                if type(sessionID) == Session_ID:
                    print u'SessionID.user: ', sessionID.user
                if type(email) == Email:
                    print u'Email.user: ', email.user
                print u'Phone.user: ', phone.user

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

    if isinstance(email, unicode) or not email:  # type(email, ) == 'unicode':
        print 'email type: ', type(email, ), 'email: ', email
    else:
        print 'email type: ', type(email, ), 'email: ', email.email

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
        print 'Order.Pk:', order.pk, ' last_name: ', last_name, ' type: ', type(last_name)
        if type(last_name, ) == list:
            last_name = unicode(last_name[0], )  # .encode('UTF8', ),
        print 'Order.Pk:', order.pk, ' last_name: ', last_name, ' type: ', type(last_name)
        last_name = last_name.lstrip('.')
        if len(last_name, ) > 30:
            print 'Order.Pk:', order.pk, ' last_name: ', last_name, ' type: ', type(last_name)
            last_name = last_name[:30]

    if first_name:
        print 'Order.Pk:', order.pk, ' first_name: ', first_name, ' type: ', type(first_name)
        if type(first_name, ) == list:
            first_name = unicode(first_name, ).encode('utf-8')
        print 'Order.Pk:', order.pk, ' first_name: ', first_name, ' type: ', type(first_name)
        first_name = first_name.lstrip('.')
        if len(first_name, ) > 30:
            print 'Order.Pk:', order.pk, ' first_name: ', first_name, ' type: ', type(first_name)
            first_name = first_name[:30]

    if patronymic:
        print 'Order.Pk:', order.pk, ' patronymic: ', patronymic, ' type: ', type(patronymic, ), 'len: ', len(patronymic, )
        if type(patronymic, ) == list:
            patronymic = unicode(patronymic, ).encode('utf-8')
        print 'Order.Pk:', order.pk, ' patronymic: ', patronymic, ' type: ', type(patronymic, ), 'len: ', len(patronymic, )
        patronymic = patronymic.lstrip('.')
        if len(patronymic, ) > 32:
            print 'Order.Pk:', order.pk, ' patronymic: ', patronymic, ' type: ', type(patronymic, ), 'len: ', len(patronymic, )
            patronymic = patronymic[:32]
        print 'Order.Pk:', order.pk, ' patronymic: ', patronymic, ' type: ', type(patronymic, ), 'len: ', len(patronymic, )

    username = ''.join(['%s' % slugify(k).capitalize() for k in last_name, first_name, patronymic], )
    print 'Order.Pk:', order.pk, ' username: ', username, ' type: ', type(username)

    if type(username, ) == list:
        username = str(username, )
    print 'Order.Pk:', order.pk, ' username: ', username, ' type: ', type(username)

    if len(username, ) > 32:
        print 'Order.Pk:', order.pk, ' username: ', username, ' type: ', type(username)
        username = username[:32]

    return username, first_name, last_name, patronymic


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
