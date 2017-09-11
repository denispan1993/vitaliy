# -*- coding: utf-8 -*-
from time import sleep
from datetime import datetime
import email as email_utils
from django.template.loader import render_to_string
from django.utils import timezone
from django.core import mail
from celery.utils.log import get_task_logger


from proj.celery import celery_app
import proj.settings

from applications.account.models import Session_ID
from applications.authModel.models import User
from .utils import get_and_render_template, get_email, get_phone, processing_username, send_email
from applications.authModel.models import Email

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
               from_email=email_utils.utils.formataddr((u'Интернет магазин Keksik', u'site@keksik.com.ua')),
               to_emails=[email_utils.utils.formataddr((u'Email zakaz@ Интернет магазин Keksik', u'zakaz@keksik.com.ua')), ],
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
        from_email=email_utils.utils.formataddr((u'Интернет магазин Keksik', u'site@keksik.com.ua')),
        to_emails=[email_utils.utils.formataddr((order.FIO, order.email)), ],
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


@celery_app.task()
def send_reminder_about_us(*args, **kwargs):

    # from datetime import timedelta
    # from django.utils import timezone
    from applications.authModel.models import Email
    from applications.delivery2.models import Delivery
    from applications.delivery.models import SpamEmail, MailAccount
    from applications.delivery2.models import Delivery, Message as modelMessage
    from applications.delivery2.message import Message as classMessage

    backend = mail.backends.smtp.EmailBackend(
        host='192.168.1.95',
        port=465,
        username=proj.settings.EMAIL_HOST_USER,
        password=proj.settings.EMAIL_HOST_PASSWORD,
        use_tls=False,
        fail_silently=False,
        use_ssl=True,
        timeout=30,
        ssl_keyfile=None,
        ssl_certfile=None, )

    """ Берем все Email's пользователи которых сделали заказ за 62 дня до сегодня """
    #try:
    #    emails = Email.objects\
    #        .filter(user__user_order__created_at__lte=timezone.now()-timedelta(days=62))
    #    emails = set(emails)
    #except Email.DoesNotExist:
    #    return False

    try:
        """ Исключаем:
            1. Тестовая рассылка и она отослана.
            2. Не тестовая рассылка и она отослана.
        """
        #delivery = Delivery.objects\
        #    .get(~Q(delivery_test=True, send_test=True, send_spam=False) | \
        #         ~Q(delivery_test=False, send_test=True, send_spam=True), pk=delivery_pk, )
        delivery = Delivery.objects.get(system_name='send_remainder_about_us', type=1, )
    except Delivery.DoesNotExist:
        return False

    email1 = Email.objects.get(pk=5301)
    email2 = Email.objects.get(pk=4009)

    for email in [email1, email2]:

        logger.info('email.email: ', email.email,
              ' bool: ', email.email is 'alex.starov@keksik.com.ua',
              ' bool: ', 'keksik.com.ua' in email.email,
              ' email: ', 'alex.starov@keksik.com.ua')

        message = classMessage(
            delivery=delivery,
            recipient_class=str('{0}.{1}'.format(Email._meta.app_label, Email._meta.model_name, ), ),
            recipient_pk=email.pk,
        )
        mail_account = MailAccount.objects.get(pk=36, )

        message.render_template(user=email.user, )
        message.create_msg()

        if message.connect(sender=mail_account, ):
            if message.send():
                message.save()
            else:
                message.delete()
        sleep(10)
        # """ Отправка напоминания о том, что клиент давно не заходил к нам """
        # template_name = kwargs.pop('email_template_name_send_reminder_about_us',
        #                            proj.settings.EMAIL_TEMPLATE_NAME['SEND_REMINDER_ABOUT_US'], )
        # logger.info('template_name: ', template_name, )

        #html_content = get_and_render_template(user=user, template_name=template_name)

        #logger.info('html_content: ', html_content)

        #send_email(
        #    subject=u'Вы давно к нам не заходили!!! Ваш магазин Кексик&nbsp;&hearts;&nbsp;&hearts;&nbsp;&hearts;',
        #    from_email=email_utils.utils.formataddr((u'Интернет магазин Keksik', u'site@keksik.com.ua')),
        #    to_emails=[email_utils.utils.formataddr((
        #        '%s %s' % (user.first_name, user.last_name, ),
        #        email.email, )), ],
        #    html_content=html_content,
        #    ext_backend=backend, )

    return True
