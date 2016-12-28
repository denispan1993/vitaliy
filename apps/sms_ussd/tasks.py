# -*- coding: utf-8 -*-
import os
import socket
import base64
from proj.celery import celery_app
from django.utils import timezone
from email.utils import formataddr
from celery.utils.log import get_task_logger
from django.core.mail import EmailMultiAlternatives
from smtplib import SMTP_SSL, SMTPException, SMTPServerDisconnected, SMTPSenderRefused, SMTPDataError

import asterisk.manager

import proj.settings

from .models import SMS, Template
from .utils import increase_send_sms

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

            response = manager.command(u'dongle sms {device} {to_phone_char} {message}'
                                       .format(
                                            device='Vodafone1',
                                            to_phone_char='+380{code}{phone}'
                                                .format(
                                                    code=sms.to_code,
                                                    phone=sms.to_phone,
                                                ),
                                            message=sms.message,
                                        ),
            )

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

    print('increase_send_sms(): ', increase_send_sms())

    return True, timezone.now(), '__name__: {0}'.format(str(__name__))


@celery_app.task(name='celery_task_send_received_sms')
def send_received_sms(*args, **kwargs):

    try:
        smses = SMS.objects.filter(direction=1, is_send=False, )
    except SMS.DoesNotExist:
        return False

    print len(smses)
    for sms in smses:

        #try:
        #    message = sms.message.encode('cp1252', 'replace')
        #except UnicodeDecodeError as e:
        #    print e
        #    message = sms.message

        sms.message = base64.b64decode(sms.message_b64).decode('utf8')

        message = u'Направление: {direction}\nОт аббонента: {from_phone_char}\nАббоненту: {to_phone_char}\n'\
                  u'Дата и Время Получения: {received_at}\nСообщение:\n{message}'\
            .format(
                direction=SMS.DIRECTION[sms.direction-1][1],
                from_phone_char=sms.from_phone_char,
                to_phone_char=sms.to_phone_char,
                received_at=sms.received_at,
                message=sms.message,
            )

        message_kwargs = {
            'from_email': formataddr((u'Телефонная станция Asterisk Keksik', 'site@keksik.com.ua', ), ),
            'to': [formataddr((u'Менеджер магазина Keksik', 'site@keksik.com.ua', ), ), ],
            #'headers': self.headers,
            'subject': u'Направение SMS: {direction} | от аббонента: {from_phone_char} | к аббоненту: {to_phone_char} | дата и время получения сообщения: {received_at}'\
                .format(
                    direction=SMS.DIRECTION[sms.direction-1][1],
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
                msg=message.message().as_string(), )
            connection.quit()

        except SMTPSenderRefused as e:
            print('SMTPSenderRefused: ', e)

        except SMTPDataError as e:
            print('SMTPDataError: ', e, ' messages: ', e.message, ' smtp_code: ', e.smtp_code, 'smtp_error: ', e.smtp_error, ' args: ', e.args)

        except Exception as e:
            print('Exception1: ', e)

        sms.task_id = None
        sms.is_send = True
        sms.send_at = timezone.now()
        sms.save(skip_super_save=True, )

    return True, timezone.now(), '__name__: {0}'.format(str(__name__))


@celery_app.task(name='celery_task_send_template_sms')
def send_template_sms(*args, **kwargs):

    to_phone_char = kwargs.pop('sms_to_phone_char', False, )
    print('sms_to_phone_char: ', to_phone_char)
    if not to_phone_char:
        return False

    template_name = kwargs.pop('sms_template_name', False, )
    try:
        print('template_name: ', template_name)
        teplate = Template.objects.get(name=template_name, )
    except Template.DoesNotExist:
        return False

    template_dict = {}
    print '203', template_dict
    for key, value in kwargs.iteritems():
        print '205', key, value
        if key.startswith('sms_'):
            print '207', "key.lstrip('sms_')", key.lstrip('sms_')
            print '208', template_dict
            template_dict.update({key.lstrip('sms_'): value})
            print '210', template_dict

    message = teplate.template.format(**template_dict)
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

            response = manager.command(u'dongle sms {device} {to_phone_char} {message}'
                                       .format(
                                            device='Vodafone1',
                                            to_phone_char=to_phone_char,
                                            message=message,
                                        ),
            )
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

    sms = SMS(template=teplate,
              direction=2,
              task_id=None,
              is_send=True,
              to_phone_char=to_phone_char,
              message=message,
              send_at=timezone.now(),
              )
    sms.save(skip_super_save=True, )

    print('increase_send_sms(): ', increase_send_sms())

    return True, timezone.now(), '__name__: {0}'.format(str(__name__))
