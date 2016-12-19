# -*- coding: utf-8 -*-
import os
from proj.celery import celery_app
from datetime import datetime, timedelta
from celery.utils.log import get_task_logger
import time


from time import sleep

from django.db.models import Q

from .models import SMS

__author__ = 'AlexStarov'

logger = get_task_logger(__name__)

PROJECT_PATH = os.path.abspath(os.path.dirname(__name__), )

path = lambda base: os.path.abspath(
    os.path.join(
        PROJECT_PATH, base
    ).replace('\\', '/')
)


@celery_app.task()
def send_sms(*args, **kwargs):
    sms_pk = kwargs.get('sms_pk')

    try:
        sms = SMS.objects.get(pk=sms_pk, is_send=False, )
    except SMS.DoesNotExist:
        print 'sms empty', sms_pk
        sms = SMS.objects.get(pk=sms_pk,)
        print sms
        print sms.is_send
        return False

    print 'SMS: ', sms

    import asterisk.manager
    import sys

    manager = asterisk.manager.Manager()

    try:
        # connect to the manager
        try:
            manager.connect('192.168.1.99')
            manager.login('web', 'mysecret123321')

            # get a status report
            response = manager.status()
            print('response: ', response)

            response = manager.command('core show channels concise')
            print('response.data: ', response.data)

            response = manager.command('dongle show devices')
            print('response.data: ', response.data)

            response = manager.command('dongle ussd dongle0 *923#')
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
    sms.save(skip_super_save=True, )

    return True, datetime.now(), '__name__: {0}'.format(str(__name__))
