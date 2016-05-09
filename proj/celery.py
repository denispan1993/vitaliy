# -*- coding: utf-8 -*-
from __future__ import absolute_import
import os

from celery import Celery

__author__ = 'AlexStarov'

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proj.settings')

from django.conf import settings  # noqa

celery_app = Celery('proj')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
celery_app.config_from_object('django.conf:settings')
celery_app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

celery_app.conf.update(
    CELERY_RESULT_BACKEND='djcelery.backends.database:DatabaseBackend',
)


@celery_app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
