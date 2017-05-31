# -*- coding: utf-8 -*-
# product/apps.py

from django.apps import AppConfig
from django.db.models.signals import m2m_changed


class ProductConfig(AppConfig, ):
    name = 'apps.product'
    verbose_name = "Rock ’n’ roll"

    def ready(self):
        from .models import AdditionalInformationForPrice
        from .signals import m2m_changed_information
        m2m_changed.connect(
            receiver=m2m_changed_information,
            sender=AdditionalInformationForPrice.information.through
        )
