# -*- coding: utf-8 -*-
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from re import split

import copy
import re
import quopri
import base64
import sys
from django.core.mail import get_connection, EmailMultiAlternatives
from django.core.mail.utils import DNS_NAME
from django.db.models import Q
from django.core.cache import cache
try:
    from django.db.models.loading import get_model
except (ImportError, ModuleNotFoundError):
    from django.apps import apps
    get_model = apps.get_model
from django.utils.html import strip_tags
from smtplib import SMTP, SMTP_SSL, SMTPException, SMTPServerDisconnected, SMTPSenderRefused, SMTPDataError
from random import randrange, randint
from datetime import datetime, timedelta
from time import mktime, sleep
from logging import getLogger
from email.utils import formataddr
from dns.resolver import Resolver, NXDOMAIN, NoAnswer, NoNameservers
import dns.resolver
from collections import OrderedDict

from django.core.cache import cache

__author__ = 'AlexStarov'

std_logger = getLogger(__name__)


def cache_get_or_set(key,
                     value,
                     timeout, ):
    try:
        return cache.get_or_set(
            key=key,
            value=value,
            timeout=timeout, )

    except AttributeError:
        cache_value = cache.get(
            key=key, )

        if not cache_value:
            cache.set(
                key=key,
                value=value,
                timeout=timeout, )
        return cache_value if cache_value else value


def get_mx_es(domain, ):
    answers = dns.resolver.query(domain, 'MX')
    mx_dict = {rdata.preference: rdata.exchange.to_text().rstrip('.') for rdata in answers}
    # for rdata in answers:
    #     print('has preference: ', rdata.preference, ' Host: ', rdata.exchange, )
    return OrderedDict(sorted(mx_dict.items()))

dict_timeouts = {
    'mail.ru': 10,
    'yandex.ru': 10,
    'yandex.net': 10,
    'rambler.ru': 10,
    'google.com': 10,
    'hotmail.com': 10,
    'yahoodns.net': 10,
    'ukr.net': 10,
    'i.ua': 10,
    'qip.ru': 10,
    'port25.com': 10,
    'mk.ua': 10,
}


def allow_to_send(domain, ):
    smtp_host = get_mx_es(domain=domain, ).items()[0][1]

    key = smtp_host.rsplit('.', 2, )[-2:]
    key = '.'.join(key, )

    if cache.get(key='allow_to_send_{0}'.format(key, ), default=False, ):
        return False

    if key in dict_timeouts:
        timeout = dict_timeouts[key]
    else:
        print('key : ', key, ' not found in dict_timeouts ', '--> smtp_host : ', smtp_host, )
        timeout = 60

    cache.set(key='allow_to_send_{0}'.format(key, ), value=True, timeout=timeout, )

    return True
