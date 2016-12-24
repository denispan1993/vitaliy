# -*- coding: utf-8 -*-
from django.core.cache import cache
from django.utils import timezone

__author__ = 'AlexStarov'


def increase_send_sms():

    value = cache.get(
        key='date_send_sms_{0}'.format(timezone.now().strftime('%Y_%m_%d'), ),
        default=False, )

    if not value:
        value = 1
        cache.set(
            key='date_send_sms_{0}'.format(timezone.now().strftime('%Y_%m_%d'), ),
            value=value,
            timeout=259200, )  # 60 sec * 60 min * 24 hour * 3
    else:
        value += 1
        cache.set(
            key='date_send_sms_{0}'.format(timezone.now().strftime('%Y_%m_%d'), ),
            value=value,
            timeout=259200, )  # 60 sec * 60 min * 24 hour * 3

    return value
