# -*- coding: utf-8 -*-
import os
import base64
import time
from datetime import timedelta
from proj.celery import celery_app
from messaging.sms import SmsSubmit
from django.utils import timezone
from email.utils import formataddr
from celery.utils.log import get_task_logger

import asterisk.manager

from django.conf import settings

from .models import SMS, Template
from .utils import increase_send_sms, send_mail

__author__ = 'AlexStarov'

logger = get_task_logger(__name__)

PROJECT_PATH = os.path.abspath(os.path.dirname(__name__), )

path = lambda base: os.path.abspath(
    os.path.join(
        PROJECT_PATH, base
    ).replace('\\', '/')
)


def decorate(func):
    start = time.time()
    print('print: Декорируем ext1 %s(*args, **kwargs): | Start: %s' % (func.__name__, start, ), )
    logger.info('logger: Декорируем ext1 %s... | Start: %s' % (func.__name__, start, ), )

    def wrapped(*args, **kwargs):
        start_int = time.time()
        print('print: Декорируем int2 %s(*args, **kwargs): | Start: %s' % (func.__name__, start_int,), )
        logger.info('logger: Декорируем int2 %s... | Start: %s' % (func.__name__, start_int,), )

        print('print: Вызываем обёрнутую функцию с аргументами: *args и **kwargs ', )
        logger.info('logger: Вызываем обёрнутую функцию с аргументами: *args и **kwargs ', )
        result = func(*args, **kwargs)

        stop_int = time.time()
        print('print: выполнено! | Stop: %s | Running time: %s' % (stop_int, stop_int - start_int,), )
        logger.info('logger: выполнено! | Stop: %s | Running time: %s' % (stop_int, stop_int - start_int,), )

        return result

    stop = time.time()
    print('print: выполнено! | Stop: %s | Running time: %s' % (stop, stop - start, ), )
    logger.info('logger: выполнено! | Stop: %s | Running time: %s' % (stop, stop - start, ), )

    return wrapped


@celery_app.task(name='sms_ussd.tasks.send_sms', )
@decorate
def send_sms(*args, **kwargs):
    sms_pk = kwargs.get('sms_pk')

    try:
        sms_inst = SMS.objects.get(pk=sms_pk, is_send=False, )
    except SMS.DoesNotExist:
        return False

    manager = asterisk.manager.Manager()

    # connect to the manager
    try:
        manager.connect(settings.ASTERISK_HOST)
        manager.login(*settings.ASTERISK_AUTH)

        # get a status report
        response = manager.status()
        print('print: response: ', response)
        logger.info('logger: response: %s' % response)
        # Success
        number = '+380{code}{phone}'\
            .format(
                code=sms_inst.to_code,
                phone=sms_inst.to_phone,
            )

        sms_to_pdu = SmsSubmit(number=number, text=sms_inst.message, )

        sms_to_pdu.request_status = True
        sms_to_pdu.validity = timedelta(days=2)
        sms_list = sms_to_pdu.to_pdu()

        # last_loop = len(sms_list) - 1
        for i, pdu_sms in enumerate(sms_list):
            time.sleep(0.5)
            response = manager.command('dongle pdu {device} {pdu}'
                                       .format(
                                            device='Vodafone1',
                                            pdu=pdu_sms.pdu,
                                        ),
                                       )
            print('print: response.data: ', response.data)
            logger.info('logger: response.data: %s' % response.data)
            # [Vodafone1] SMS queued for send with id 0x7f98c8004420\n--END COMMAND--\r\n
            sended_sms = increase_send_sms()
            print('print: sended SMS: ', sended_sms)
            logger.info('logger: sended SMS: %s' % sended_sms)
            # if i != last_loop:
            #     time.sleep(1.5)
            time.sleep(0.5)

        manager.logoff()

    except asterisk.manager.ManagerSocketException as e:
        print("Error connecting to the manager: %s" % e, )
    except asterisk.manager.ManagerAuthException as e:
        print("Error logging in to the manager: %s" % e, )
    except asterisk.manager.ManagerException as e:
        print("Error: %s" % e, )

    finally:
        # remember to clean up
        try:
            manager.close()
        except Exception as e:
            print('print: sms_ussd/task.py: e: ', e)
            logger.info('logger: sms_ussd/task.py: e: %s' % e)

    sms_inst.task_id = None
    sms_inst.is_send = True
    sms_inst.send_at = timezone.now()
    sms_inst.save(skip_super_save=True, )

    return True, timezone.now(), '__name__: {0}'.format(str(__name__))


@celery_app.task(name='sms_ussd.tasks.send_received_sms', )
@decorate
def send_received_sms(*args, **kwargs):

    try:
        smses = SMS.objects.filter(direction=1, is_send=False, )
    except SMS.DoesNotExist:
        return False

    logger.info(len(smses), )
    send_sms_successful = True
    for sms in smses:

        sms.message = base64.b64decode(sms.message_b64).decode('utf8')

        subject = 'Направение SMS: {direction} | от аббонента: {from_phone_char} | к аббоненту: {to_phone_char} '\
                  '| дата и время получения сообщения: {received_at}'\
            .format(
                direction=SMS.DIRECTION[sms.direction-1][1],
                from_phone_char=sms.from_phone_char,
                to_phone_char=sms.to_phone_char,
                received_at=sms.received_at,
            )

        message = 'Направление: {direction}\nОт аббонента: {from_phone_char}\nАббоненту: {to_phone_char}\n'\
                  'Дата и Время Получения: {received_at}\nСообщение:\n{message}'\
            .format(
                direction=SMS.DIRECTION[sms.direction-1][1],
                from_phone_char=sms.from_phone_char,
                to_phone_char=sms.to_phone_char,
                received_at=sms.received_at,
                message=sms.message,
            )

        message_kwargs = {
            'from_email': formataddr(('Телефонная станция Asterisk Keksik', 'site@keksik.com.ua', ), ),
            'to': [formataddr(('Менеджер магазина Keksik', 'site@keksik.com.ua', ), ), ],
            'subject': subject,
            'body': message,
        }

        if send_mail(**message_kwargs):

            sms.sim_id = 255016140761290
            sms.task_id = None
            sms.is_send = True
            sms.send_at = timezone.now()
            sms.save(skip_super_save=True, )

        else:
            send_sms_successful = False

    if send_sms_successful:
        return True, timezone.now(), '__name__: {0}'.format(str(__name__))
    else:
        return False, timezone.now(), '__name__: {0}'.format(str(__name__))


@celery_app.task(name='sms_ussd.task.send_template_sms')
@decorate
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
        template = Template.objects.get(name=template_name, )
    except Template.DoesNotExist:
        return False

    template_dict = {}

    for key, value in kwargs.items():

        if key.startswith('sms_'):

            template_dict.update({key.lstrip('sms_'): value})

    message = template.template.format(**template_dict)

    sms_inst = SMS(template=template,
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

    # connect to the manager
    try:
        manager.connect(settings.ASTERISK_HOST)
        manager.login(*settings.ASTERISK_AUTH)

        # get a status report
        response = manager.status()
        print('response: ', response)

        number = '+380{code}{phone}'\
            .format(
                code=sms_inst.to_code,
                phone=sms_inst.to_phone,
            )

        sms_to_pdu = SmsSubmit(number=number, text=sms_inst.message, )

        sms_to_pdu.request_status = False
        sms_to_pdu.validity = timedelta(days=2)
        sms_list = sms_to_pdu.to_pdu()

        # last_loop = len(sms_list) - 1
        for i, pdu_sms in enumerate(sms_list):
            time.sleep(0.5)
            response = manager.command('dongle pdu {device} {pdu}'
                                       .format(
                                            device='Vodafone1',
                                            pdu=pdu_sms.pdu,
                                        ),
                                       )
            print('print: response.data: ', response.data)
            logger.info('logger: response.data: %s' % response.data)
            # [Vodafone1] SMS queued for send with id 0x7f98c8004420\n--END COMMAND--\r\n
            sended_sms = increase_send_sms()
            print('print: sended SMS: ', sended_sms)
            logger.info('logger: sended SMS: %s' % sended_sms)
            # if i != last_loop:
            #     time.sleep(1.5)
            time.sleep(0.5)

        manager.logoff()

    except asterisk.manager.ManagerSocketException as e:
        print("Error connecting to the manager: %s" % e, )
    except asterisk.manager.ManagerAuthException as e:
        print("Error logging in to the manager: %s" % e, )
    except asterisk.manager.ManagerException as e:
        print("Error: %s" % e, )

    finally:
        # remember to clean up
        try:
            manager.close()
        except Exception as e:
            print('sms_ussd/tasks.py: e: ', e, )

    sms_inst.save(skip_super_save=True, )

    return True, timezone.now(), '__name__: {0}'.format(str(__name__))
