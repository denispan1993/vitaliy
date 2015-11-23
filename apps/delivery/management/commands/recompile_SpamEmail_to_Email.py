# -*- coding: utf-8 -*-
__author__ = 'AlexStarov'

from django.core.management.base import BaseCommand


class Command(BaseCommand, ):
    def handle(self, *args, **options):
        from apps.authModel.models import Email
        from apps.delivery.models import TraceOfVisits
        visits = TraceOfVisits.objects.all()
        for visit in visits:
            try:
                email = Email.objects.get(email=visit.email.now_email.email, )
            except Email.DoesNotExist:
                print visit.email.now_email.email
                print 'Description: ', 'From apps.delivery.model.SpamEmail'
            else:
                print email
