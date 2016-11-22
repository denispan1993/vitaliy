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
from django.db.models.loading import get_model
from django.utils.html import strip_tags
from smtplib import SMTP, SMTP_SSL, SMTPException, SMTPServerDisconnected, SMTPSenderRefused, SMTPDataError
from random import randrange, randint
from datetime import datetime, timedelta
from time import mktime, sleep
from logging import getLogger
from email.utils import formataddr
from dns.resolver import Resolver, NXDOMAIN, NoAnswer, NoNameservers

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
