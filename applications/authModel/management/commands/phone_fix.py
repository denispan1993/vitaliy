# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand

from applications.authModel.models import Phone

__author__ = 'AlexStarov'
""" Фиксим телефоны. """


class Command(BaseCommand, ):

    def handle(self, *args, **options):

        for phone in Phone.objects.all():

            if len(phone.phone) == 9:

                try:
                    phone.int_code = int(phone.phone[:2])
                    phone.int_phone = int(phone.phone[2:])
                except ValueError:
                    continue
            else:
                continue

            phone.save()
