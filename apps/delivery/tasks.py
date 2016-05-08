# -*- coding: utf-8 -*-
from proj.celery import app as celery_app
from datetime import datetime, timedelta
from logging import getLogger

__author__ = 'AlexStarov'

debug_log = getLogger('celery')


@celery_app.task(run_every=timedelta(seconds=1))
def test():
    print 'All work!!!'
    debug_log.info(u'message: {0}, datetime: {1}'.format('All Work', datetime.now()))

