# -*- coding: utf-8 -*-
# product/apps.py

from django.apps import AppConfig
from django.db.models.signals import pre_save


class CartConfig(AppConfig, ):
    name = 'apps.cart'
    verbose_name = "Rock ’n’ roll"

    def ready(self):
        from apps.coupon.models import CouponGroup
        from .signals import my_pre_save
        pre_save.connect(
            receiver=my_pre_save,
            sender=CouponGroup,
        )
