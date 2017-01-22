# -*- coding: utf-8 -*-
import os
import socket
import base64
import time
from datetime import timedelta
from proj.celery import celery_app
from messaging.sms import SmsSubmit
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
        sms_inst = SMS.objects.get(pk=sms_pk, is_send=False, )
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

            number = '+380{code}{phone}'\
                .format(
                    code=sms_inst.to_code,
                    phone=sms_inst.to_phone,
                )

            sms_to_pdu = SmsSubmit(number=number, text=sms_inst.message, )

            sms_to_pdu.request_status = True
            sms_to_pdu.validity = timedelta(days=4)
            sms_list = sms_to_pdu.to_pdu()

            last_loop = len(sms_list) - 1
            for i, pdu_sms in enumerate(sms_list):
                response = manager.command(u'dongle pdu {device} {pdu}'
                                           .format(
                                                device='Vodafone1',
                                                pdu=pdu_sms.pdu,
                                            ),
                                           )
                print('response.data: ', response.data)

                increase_send_sms()
                if i != last_loop:
                    time.sleep(10)

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

    sms_inst.task_id = None
    sms_inst.is_send = True
    sms_inst.send_at = timezone.now()
    sms_inst.save(skip_super_save=True, )

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

        subject = u'Направение SMS: {direction} | от аббонента: {from_phone_char} | к аббоненту: {to_phone_char} '\
                  u'| дата и время получения сообщения: {received_at}'\
                .format(
                    direction=SMS.DIRECTION[sms.direction-1][1],
                    from_phone_char=sms.from_phone_char,
                    to_phone_char=sms.to_phone_char,
                    received_at=sms.received_at,
                ),

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
            'subject': subject,
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

        sms.sim_id = 255016140761290
        sms.task_id = None
        sms.is_send = True
        sms.send_at = timezone.now()
        sms.save(skip_super_save=True, )

    return True, timezone.now(), '__name__: {0}'.format(str(__name__))


@celery_app.task(name='celery_task_send_template_sms')
def send_template_sms(*args, **kwargs):

    phone = kwargs.pop('sms_to_phone_char', False, )
    if not phone:
        return False

    phone = phone.replace(' ', '').strip('+') \
        .replace('(', '').replace(')', '').replace('-', '') \
        .lstrip('380').lstrip('38').lstrip('80').lstrip('0')

    try:
        int_phone = int(phone[2:])
        int_code = int(phone[:2])
    except ValueError:
        return False

    template_name = kwargs.pop('sms_template_name', False, )
    try:
        teplate = Template.objects.get(name=template_name, )
    except Template.DoesNotExist:
        return False

    template_dict = {}

    for key, value in kwargs.iteritems():

        if key.startswith('sms_'):

            template_dict.update({key.lstrip('sms_'): value})

    message = teplate.template.format(**template_dict)

    sms_inst = SMS(template=teplate,
                   direction=2,
                   task_id=None,
                   sim_id=255016140761290,
                   is_send=True,
                   message=message,
                   to_phone_char=phone,
                   to_code=int_code,
                   to_phone=int_phone,
                   send_at=timezone.now(),
                   )

    manager = asterisk.manager.Manager()

    try:
        # connect to the manager
        try:
            manager.connect(proj.settings.ASTERISK_HOST)
            manager.login(*proj.settings.ASTERISK_AUTH)

            # get a status report
            response = manager.status()
            print('response: ', response)

            number = '+380{code}{phone}'\
                .format(
                    code=sms_inst.to_code,
                    phone=sms_inst.to_phone,
                )

            sms_to_pdu = SmsSubmit(number=number, text=sms_inst.message, )

            sms_to_pdu.request_status = True
            sms_to_pdu.validity = timedelta(days=4)
            sms_list = sms_to_pdu.to_pdu()

            last_loop = len(sms_list) - 1
            for i, pdu_sms in enumerate(sms_list):
                response = manager.command(u'dongle pdu {device} {pdu}'
                                           .format(
                                                device='Vodafone1',
                                                pdu=pdu_sms.pdu,
                                            ),
                                           )
                print('response.data: ', response.data)

                increase_send_sms()
                if i != last_loop:
                    time.sleep(10)

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

    sms_inst.save(skip_super_save=True, )

    return True, timezone.now(), '__name__: {0}'.format(str(__name__))
