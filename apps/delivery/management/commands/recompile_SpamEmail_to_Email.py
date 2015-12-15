# -*- coding: utf-8 -*-
__author__ = 'AlexStarov'

from django.core.management.base import BaseCommand

""" Копируем все Email адреса с которых пришли к нам по рассылкам в основную базу Email-ов """
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
                email.save()
            else:
                print i, ' ', email
            i += 1
        """ Закрываем адреса которые мы перенесли в основную базу """
        from apps.delivery.models import SpamEmail
        emails = Email.objects.all()
        for email in emails:
            try:
                email = email.email
            except AttributeError:
                continue
            try:
                email = SpamEmail.objects.get(email=email, )
            except SpamEmail.DoesNotExist:
                print 'AllOk'
            else:
                email.bad_email = True
                email.save()
