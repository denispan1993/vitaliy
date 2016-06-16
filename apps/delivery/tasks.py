# -*- coding: utf-8 -*-
from proj.celery import celery_app
from datetime import datetime, timedelta
from logging import getLogger
from celery.utils.log import get_task_logger

from apps.delivery.models import Delivery

__author__ = 'AlexStarov'

debug_log = getLogger('celery')
logger = get_task_logger(__name__)
std_logger = getLogger(__name__)


@celery_app.task()
def processing_delivery(*args, **kwargs):
    for key, value in kwargs.items():
        print key, ': ', value
    delivery_type = kwargs.get('delivery_type')
    print 'delivery_type: ', delivery_type
    delivery = kwargs.get('delivery')
    print 'delivery: ', delivery

    delivery = Delivery.objects.get(pk=delivery, )
    print 'delivery: ', delivery

    print 'All work!!!'
    logger.info(u'message: datetime.now() {0}'.format(datetime.now()))
    # std_logger.info(u'message: datetime.now() {0}'.format(datetime.now()))
    debug_log.info(u'message: {0}, datetime: {1}'.format('All Work', datetime.now()))
    return True, datetime.now()


@celery_app.task(run_every=timedelta(seconds=1))
def test():
    print 'All work!!!'
    logger.info(u'message: datetime.now() {0}'.format(datetime.now()))
    # std_logger.info(u'message: datetime.now() {0}'.format(datetime.now()))
    debug_log.info(u'message: {0}, datetime: {1}'.format('All Work', datetime.now()))
    return True, datetime.now()

