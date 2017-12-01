# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand

from applications.yml import tasks

__author__ = 'AlexStarov'


class Command(BaseCommand, ):

    def handle(self, *args, **options):

        tasks.generate_prom_ua_yml.apply_async(queue='celery', )
