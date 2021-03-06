# -*- coding: utf-8 -*-
# account/applications.py

from django.apps import AppConfig


class AccountConfig(AppConfig, ):
    name = 'applications.account'
    verbose_name = "Учетные записи"

    def ready(self):
        from django.db.models.signals import post_save
        from .signals import AutoCreate_UserProfileModel
        from django.conf import settings
        post_save.connect(
            receiver=AutoCreate_UserProfileModel,
            sender=settings.AUTH_USER_MODEL,
        )
