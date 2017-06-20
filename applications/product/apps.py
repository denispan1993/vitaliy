# -*- coding: utf-8 -*-
# product/applications.py

from django.apps import AppConfig
from django.db.models.signals import m2m_changed


class ProductConfig(AppConfig, ):
    name = 'applications.product'
    verbose_name = "Продукты и категории"

    def ready(self):
        from .models import AdditionalInformationForPrice
        from .signals import m2m_changed_information
        m2m_changed.connect(
            receiver=m2m_changed_information,
            sender=AdditionalInformationForPrice.information.through
        )
