# -*- coding: utf-8 -*-

from .status_process import success
from .conf import settings

__author__ = 'AlexStarov'


def check_auth(request):
    session = request.session
    success_text = '{}\n{}'.format(settings.SESSION_COOKIE_NAME, session.session_key)
    return success(success_text)
