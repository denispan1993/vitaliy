# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand

__author__ = 'AlexStarov'


class Command(BaseCommand, ):

    def handle(self, *args, **options):
        from django.contrib.sessions.models import Session

        import datetime

        datetime_object = datetime.datetime(2017, 1, 1).\
            replace(tzinfo=datetime.timezone(datetime.timedelta(hours=-3)))

        # aaa = Session.objects.filter(expire_date__lt=datetime_object).delete()
        # print(aaa)
        aaa = Session.objects.filter(expire_date__lt=datetime_object).count()  # datetime.datetime.now()
        print(aaa)
        # print(len(aaa))

