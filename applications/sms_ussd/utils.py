# -*- coding: utf-8 -*-
from django.core.cache import cache
#from django.utils import timezone
from datetime import date

__author__ = 'AlexStarov'


def increase_send_sms():

    # key = 'date_send_sms_{0}'.format(timezone.now().strftime('%Y_%m_%d'), ),
    key = 'date_send_sms_{0}'.format(date.today().strftime('%Y_%m_%d'), ),
    value = cache.get(
        key=key,
        default=False, )

    if not value:
        value = 1
        cache.set(
            key=key,
            value=value,
            timeout=259200, )  # 60 sec * 60 min * 24 hour * 3
    else:
        value += 1
        cache.set(
            key=key,
            value=value,
            timeout=259200, )  # 60 sec * 60 min * 24 hour * 3

    print('key: ', key, ' value: ', value, )

    return value
