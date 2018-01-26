# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand

from applications.sms_ussd import tasks

__author__ = 'AlexStarov'


class Command(BaseCommand, ):

    def handle(self, *args, **options):

        tasks.send_received_sms.apply_async(queue='celery', )
