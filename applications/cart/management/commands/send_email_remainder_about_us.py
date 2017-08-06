# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
import celery

from applications.cart.tasks import send_reminder_about_us

__author__ = 'AlexStarov'
""" Запускаем задачу по отправке "Напоминания о том, что мы существуеи". """


class Command(BaseCommand, ):

    def handle(self, *args, **options):

        send_reminder_about_us.apply_async(
            queue='celery',
            task_id='celery-task-id-send_remainder_about_us-{0}'.format(celery.utils.uuid(), ),
        )
