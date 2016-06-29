# -*- coding: utf-8 -*-
from proj.celery import celery_app
from datetime import datetime, timedelta
from celery.utils.log import get_task_logger

from django.db.models import Q
from smtplib import SMTPSenderRefused, SMTPDataError

from apps.delivery.models import Delivery, EmailMiddleDelivery, EmailForDelivery
from apps.authModel.models import Email
from apps.delivery.utils import Mail_Account, get_email, create_msg, connect, send_msg

__author__ = 'AlexStarov'

logger = get_task_logger(__name__)


def send(delivery, mail_account, email, msg):
    try:
        connection = connect(mail_account=mail_account, fail_silently=False, )
        send_msg(connection=connection, mail_account=mail_account, email=email, msg=msg, )
    except SMTPSenderRefused as e:
        print('SMTPSenderRefused: ', e)
    except SMTPDataError as e:
        print('SMTPDataError: ', e)
    except Exception as e:
        print('Exception: ', e)
        if "(554, '5.7.1 Message rejected under suspicion of SPAM; http://help.yandex.ru/mail/spam/sending-limits.xml" in e:
            print('SPAM Bloked E-Mail: ', mail_account, ' NOW !!!!!!!!!!!!!!!!!!!!!!!')
            from datetime import datetime
            mail_account.is_auto_active = False
            mail_account.auto_active_datetime = datetime.now()
            mail_account.save()
        connection = connect(mail_account=mail_account, fail_silently=True, )
        msg = create_msg(delivery=delivery, mail_account=mail_account, email=email, exception=e, test=True, )
        send_msg(connection=connection, mail_account=mail_account, email=email, msg=msg, )


@celery_app.task()
def processing_delivery(*args, **kwargs):
    for key, value in kwargs.items():
        logger.info(key, ': ', value)
    delivery_type = kwargs.get('delivery_type')
    logger.info(u'delivery_type: {0}'.format(delivery_type))
    delivery_pk = kwargs.get('delivery_pk')
    logger.info(u'delivery_pk: {0}'.format(delivery_pk))

    try:
        """ Исключаем:
            1. Тестовая рассылка и она отослана.
            2. Не естовая рассылка и она отослана.
        """
        delivery = Delivery.objects\
            .get(~Q(delivery_test=True, send_test=True, send_spam=False) | \
                 ~Q(delivery_test=False, send_test=True, send_spam=True), pk=delivery_pk, )
    except Delivery.DoesNotExist:
        delivery = False

    aaa = EmailMiddleDelivery.objects.filter(delivery=delivery,
                                   delivery_test_send=True,
                                   delivery_send=False,
                                   updated_at__lte=delivery.updated_at, )
    logger.info(u'delivery aaa: {0}'.format(len(aaa)))
    if delivery and delivery_type == 'test':
        """ Создаем ссылочку на отсылку рассылки """
        email_middle_delivery = EmailMiddleDelivery.objects.create(delivery=delivery,
                                                                   delivery_test_send=True,
                                                                   delivery_send=False, )
        """ Закрываем отсылку теста в самой рассылке """
        delivery.send_test = True
        delivery.save()

        real_email = get_email(delivery=delivery, email_class=Email, pk=6, )  # pk=2836, )  # subscribe@keksik.com.ua
        email = EmailForDelivery.objects.create(delivery=email_middle_delivery,
                                                now_email=real_email,
                                                email=real_email, )
        mail_account = Mail_Account(pk=1, )
        msg = create_msg(delivery=delivery, mail_account=mail_account, email=email, test=True, )
        """ Посылаем письмо - subscribe@keksik.com.ua """
        send(delivery=delivery, mail_account=mail_account, email=email, msg=msg)

        """ Посылаем письмо - check-auth2@verifier.port25.com """
        real_email = get_email(delivery=delivery, email_class=Email, pk=7, )  # pk=3263, )  # check-auth2@verifier.port25.com
        email = EmailForDelivery.objects.create(delivery=email_middle_delivery,
                                                now_email=real_email,
                                                email=real_email, )
        send(delivery=delivery, mail_account=mail_account, email=email, msg=msg)

    else:
        kwargs_data = {'delivery_type': 'delivery', }

    logger.info(u'message: datetime.now() {0}, {1}'.format(delivery_type, delivery_pk))
    return '__name__: {0}'.format(str(__name__))


@celery_app.task(run_every=timedelta(seconds=1))
def test():
    print('All work!!!')
    logger.info(u'message: datetime.now() {0}'.format(datetime.now()))
    # std_logger.info(u'message: datetime.now() {0}'.format(datetime.now()))
    # debug_log.info(u'message: {0}, datetime: {1}'.format('All Work', datetime.now()))
    return True, datetime.now()

