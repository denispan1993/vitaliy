# -*- coding: utf-8 -*-
# product/applications.py

from django.apps import AppConfig


class DiscountConfig(AppConfig, ):
    name = 'applications.discount'
    verbose_name = "Скидки"
