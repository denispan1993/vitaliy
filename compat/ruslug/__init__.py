#! /usr/bin/env python
# -*- coding: utf-8 -*- 
from django.conf import settings
import urlparse

ALLOWED_SLUG_CHARS = u'1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZйцукенгшщзхъфывапролджэячсмитьбюЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ-'


def patch_admin_form(form):
    js_file = urlparse.urljoin(settings.MEDIA_URL, 'js/admin/ruslug-urlify.js')
    form.Media.js = form.Media.js + (js_file,)
    return form
