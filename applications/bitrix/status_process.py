# -*- coding: utf-8 -*-

import logging
from django.http import HttpResponse
from proj import settings

__author__ = 'AlexStarov'

logger = logging.getLogger(__name__)


def error(request, error_text):
    logger.error(error_text)
    result = '{}\n{}'.format(settings.CML_RESPONSE_ERROR, error_text)
    return HttpResponse(result)


def success(request, success_test=''):
    result = '{}\n{}'.format(settings.CML_RESPONSE_SUCCESS, success_test)
    return HttpResponse(result)
