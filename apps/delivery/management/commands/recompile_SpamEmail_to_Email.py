# -*- coding: utf-8 -*-
__author__ = 'AlexStarov'

from django.core.management.base import BaseCommand


class Command(BaseCommand, ):
    def handle(self, *args, **options):
        from apps.authModel.models import Email
        from apps.delivery.models import TraceOfVisits
        visits = TraceOfVisits.objects.all()
        i = 0
        for visit in visits:
            try:
                email = visit.email.now_email.email
            except AttributeError:
                continue
            try:
                email = Email.objects.get(email=email, )
            except Email.DoesNotExist:
                print i, ' ', email
                print 'Description: ', 'From apps.delivery.model.SpamEmail'
                email = Email(email=email, description='From apps.delivery.model.SpamEmail', )
            else:
                print email
            i += 1
