# -*- coding: utf-8 -*-
__author__ = 'AlexStarov'

from django.core.management.base import BaseCommand


class Command(BaseCommand, ):
    def handle(self, *args, **options):
        from apps.authModel.models import Email
        from django.contrib.contenttypes.models import ContentType
        content_type_email = ContentType.objects.get_for_model(model=Email, for_concrete_model=True, )

        from apps.delivery.models import EmailForDelivery
        emailsfordelivery = EmailForDelivery.objects.all()
        print emailsfordelivery

        for email in emailsfordelivery:
            email.object_id = email.email_id
            email.content_type = content_type_email
            print email
            email.save()
