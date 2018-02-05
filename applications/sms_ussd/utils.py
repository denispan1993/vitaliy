# -*- coding: utf-8 -*-
from datetime import date
from smtplib import SMTP_SSL, SMTPException, SMTPServerDisconnected, SMTPSenderRefused, SMTPDataError

import socket

from email.utils import formataddr
from celery.utils.log import get_task_logger

from django.conf import settings

from django.core.cache import cache
from django.core.mail import EmailMultiAlternatives

__author__ = 'AlexStarov'

logger = get_task_logger(__name__)


def increase_send_sms() -> int:

    # key = 'date_send_sms_{0}'.format(timezone.now().strftime('%Y_%m_%d'), ),
    key = 'date_send_sms_{0}'.format(date.today().strftime('%Y_%m_%d'), ),
    value = cache.get(
        key=key,
        default=False, )

    if not value:
        value = 1
        cache.set(
            key=key,
            value=value,
            timeout=259200, )  # 60 sec * 60 min * 24 hour * 3
    else:
        value += 1
        cache.set(
            key=key,
            value=value,
            timeout=259200, )  # 60 sec * 60 min * 24 hour * 3

    print('key: ', key, ' value: ', value, )

    return value


def send_mail(from_email: str, to: dict, subject: str, body: str, ):

    message = EmailMultiAlternatives(from_email=from_email, to=to, subject=subject, body=body, )

    connection_params = {'local_hostname': 'mail-proxy.keksik.com.ua', }

    try:
        connection = SMTP_SSL(
            host=settings.SEND_SMS_MAIL_ACCOUNT['server_smtp'],
            port=settings.SEND_SMS_MAIL_ACCOUNT['port_smtp'],
            **connection_params)

        if settings.SEND_SMS_MAIL_ACCOUNT['username'] \
                and settings.SEND_SMS_MAIL_ACCOUNT['password']:
            connection.login(
                settings.SEND_SMS_MAIL_ACCOUNT['username'],
                settings.SEND_SMS_MAIL_ACCOUNT['password'],
            )
            connection.ehlo()

    except (SMTPException, SMTPServerDisconnected) as e:
        logger.error('Exception(SMTPException, SMTPServerDisconnected): %s' % e)
        return False

    except socket.error as e:
        logger.info('Exception(socket.error): %s' % e)
        return False

    try:
        # (Python3) msg --> convert to bytes
        connection.sendmail(from_addr=formataddr(('Asterisk Keksik', 'site@keksik.com.ua',), ),
                            to_addrs=[formataddr(('Менеджер магазина Keksik', 'site@keksik.com.ua',), ), ],
                            msg=message.message().as_string().encode(), )
        connection.quit()

        # Если мы письмо отправили то возвращаем True
        return True

    except SMTPSenderRefused as e:
        logger.info('SMTPSenderRefused: %s' % e)

    except SMTPDataError as e:
        logger.info('SMTPDataError: %s| messages: %s| smtp_code: %s| smtp_error: %s| args: %s' %
                    (e, e.message, e.smtp_code, e.smtp_error, e.args), )

    except Exception as e:
        logger.info('Exception1: %s' % e)

    # Если письмо не ушло то возвращаем False
    return False
