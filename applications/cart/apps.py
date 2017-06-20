# -*- coding: utf-8 -*-
# product/applications.py

from django.apps import AppConfig
from django.db.models.signals import pre_save


class CartConfig(AppConfig, ):
    name = 'applications.cart'
    verbose_name = "Корзины и заказы"

    def ready(self):
        from applications.coupon.models import CouponGroup
        from .signals import my_pre_save
        pre_save.connect(
            receiver=my_pre_save,
            sender=CouponGroup,
        )
