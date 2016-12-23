# -*- coding: utf-8 -*-
import os
import socket
from proj.celery import celery_app
from django.utils import timezone
from email.utils import formataddr
from celery.utils.log import get_task_logger
from django.core.mail import EmailMultiAlternatives
from smtplib import SMTP_SSL, SMTPException, SMTPServerDisconnected, SMTPSenderRefused, SMTPDataError

import asterisk.manager

import proj.settings

from apps.delivery.models import MailAccount
from .models import SMS, Template

__author__ = 'AlexStarov'

logger = get_task_logger(__name__)

PROJECT_PATH = os.path.abspath(os.path.dirname(__name__), )

path = lambda base: os.path.abspath(
    os.path.join(
        PROJECT_PATH, base
    ).replace('\\', '/')
)


@celery_app.task(name='celery_task_send_sms')
def send_sms(*args, **kwargs):
    sms_pk = kwargs.get('sms_pk')

    try:
        print('sms_pk: ', sms_pk)
        sms = SMS.objects.get(pk=sms_pk, is_send=False, )
    except SMS.DoesNotExist:
        return False

    manager = asterisk.manager.Manager()

    try:
        # connect to the manager
        try:
            manager.connect(proj.settings.ASTERISK_HOST)
            manager.login(*proj.settings.ASTERISK_AUTH)

            # get a status report
            response = manager.status()
            print('response: ', response)

            response = manager.command('core show channels concise')
            print('response.data: ', response.data)

            response = manager.command('dongle show version')
            print('response.data: ', response.data)

            response = manager.command('dongle show devices')
            print('response.data: ', response.data)

            response = manager.command('dongle ussd Vodafone1 *161#')
            print('response.data: ', response.data)

            response = manager.command('dongle show device settings')
            print('response.data: ', response.data)

            response = manager.command('dongle show device state')
            print('response.data: ', response.data)

            response = manager.command('dongle show device statistics')
            print('response.data: ', response.data)

            manager.logoff()

        except asterisk.manager.ManagerSocketException as e:
            print "Error connecting to the manager: %s" % e
        except asterisk.manager.ManagerAuthException as e:
            print "Error logging in to the manager: %s" % e
        except asterisk.manager.ManagerException as e:
            print "Error: %s" % e

    finally:
        # remember to clean up
        try:
            manager.close()
        except Exception as e:
            print e

    sms.task_id = None
    sms.is_send = True
    sms.send_at = timezone.now()
    sms.save(skip_super_save=True, )

    return True, timezone.now(), '__name__: {0}'.format(str(__name__))


@celery_app.task(name='celery_task_send_received_sms')
def send_received_sms(*args, **kwargs):

    try:
        smses = SMS.objects.filter(direction=1, is_send=False, )
    except SMS.DoesNotExist:
        return False

    for sms in smses:
        message = 'Direction: {direction}\nFrom: {from_phone_char}\nTo: {to_phone_char}\n'\
                  'DateTime Received: {received_at}\nDateTime Sended: {send_at}\n' \
                  'Message:\n{message}'\
            .format(
                direction=sms.direction,
                from_phone_char=sms.from_phone_char,
                to_phone_char=sms.to_phone_char,
                received_at=sms.received_at,
                send_at=sms.send_at,
                message=sms.message.encode('cp1252', 'replace'),
            )

        message_kwargs = {
            'from_email': formataddr((u'Asterisk Keksik', 'site@keksik.com.ua', ), ),
            'to': [formataddr((u'Менеджер магазина Keksik', 'site@keksik.com.ua', ), ), ],
            #'headers': self.headers,
            'subject': u'SMS от: {from_phone_char} | к: {to_phone_char} | дата и время: {received_at}'\
                .format(
                    from_phone_char=sms.from_phone_char,
                    to_phone_char=sms.to_phone_char,
                    received_at=sms.received_at,
                ),
            'body': message,
        }

        message = EmailMultiAlternatives(**message_kwargs)

        connection_params = {'local_hostname': 'mail-proxy.keksik.com.ua', }

        try:
            connection = SMTP_SSL(
                host=proj.settings.SEND_SMS_MAIL_ACCOUNT['server_smtp'],
                port=proj.settings.SEND_SMS_MAIL_ACCOUNT['port_smtp'],
                **connection_params)

            if proj.settings.SEND_SMS_MAIL_ACCOUNT['username']\
                    and proj.settings.SEND_SMS_MAIL_ACCOUNT['password']:
                connection.login(
                    proj.settings.SEND_SMS_MAIL_ACCOUNT['username'],
                    proj.settings.SEND_SMS_MAIL_ACCOUNT['password'],
                )
                connection.ehlo()

        except (SMTPException, SMTPServerDisconnected) as e:
            print('Exception(SMTPException, SMTPServerDisconnected): ', e)
            return False

        except socket.error as e:
            print('Exception(socket.error): ', e)
            return False

        try:
            connection.sendmail(
                from_addr=formataddr((u'Asterisk Keksik', 'site@keksik.com.ua', ), ),
                to_addrs=[formataddr((u'Менеджер магазина Keksik', 'site@keksik.com.ua', ), ), ],
                msg=message.message(), )
            connection.quit()

        except SMTPSenderRefused as e:
            print('SMTPSenderRefused: ', e)

        except SMTPDataError as e:
            print('SMTPDataError: ', e, ' messages: ', e.message, ' smtp_code: ', e.smtp_code, 'smtp_error: ', e.smtp_error, ' args: ', e.args)

        except Exception as e:
            print('Exception: ', e)

        sms.task_id = None
        sms.is_send = True
        sms.send_at = timezone.now()
        sms.save(skip_super_save=True, )

    return True, timezone.now(), '__name__: {0}'.format(str(__name__))


@celery_app.task(name='celery_task_send_template_sms')
def send_template_sms(*args, **kwargs):

    sms_to_phone_char = kwargs.pop('sms_to_phone_char', False, )
    print('sms_to_phone_char: ', sms_to_phone_char)
    if not sms_to_phone_char:
        return False

    sms_template_name = kwargs.pop('sms_template_name', False, )
    try:
        print('sms_template_name: ', sms_template_name)
        sms_teplate = Template.objects.get(name=sms_template_name, )
    except Template.DoesNotExist:
        return False

    sms_template_dict = {}
    for key, value in kwargs.iteritems():
        if key.startswith('sms_'):
            sms_template_dict.update([key, value])

    message = sms_teplate.template.format(**sms_template_dict)
    print message

    manager = asterisk.manager.Manager()

    try:
        # connect to the manager
        try:
            manager.connect(proj.settings.ASTERISK_HOST)
            manager.login(*proj.settings.ASTERISK_AUTH)

            # get a status report
            response = manager.status()
            print('response: ', response)

            response = manager.command('core show channels concise')
            print('response.data: ', response.data)

            response = manager.command('dongle show version')
            print('response.data: ', response.data)

            response = manager.command('dongle show devices')
            print('response.data: ', response.data)

            response = manager.command('dongle ussd Vodafone1 *161#')
            print('response.data: ', response.data)

            response = manager.command('dongle show device settings')
            print('response.data: ', response.data)

            response = manager.command('dongle show device state')
            print('response.data: ', response.data)

            response = manager.command('dongle show device statistics')
            print('response.data: ', response.data)

            manager.logoff()

        except asterisk.manager.ManagerSocketException as e:
            print "Error connecting to the manager: %s" % e
        except asterisk.manager.ManagerAuthException as e:
            print "Error logging in to the manager: %s" % e
        except asterisk.manager.ManagerException as e:
            print "Error: %s" % e

    finally:
        # remember to clean up
        try:
            manager.close()
        except Exception as e:
            print e

    sms.task_id = None
    sms.is_send = True
    sms.send_at = timezone.now()
    sms.save(skip_super_save=True, )

    return True, timezone.now(), '__name__: {0}'.format(str(__name__))
