#! /usr/bin/env python
# -*- coding: utf-8 -*- 
#from django.utils.translation import ugettext_lazy as _
from django import forms
#import re
from compat.ruslug import ALLOWED_SLUG_CHARS


class RuSlugFormField(forms.CharField):
    def __init__(self, max_length=None, min_length=None, error_message=None, *args, **kwargs):
        if error_message:
            error_messages = kwargs.get('error_messages') or {}
            error_messages['invalid'] = error_message
            kwargs['error_messages'] = error_messages
        super(RuSlugFormField, self).__init__(max_length, min_length, *args, **kwargs)

    def clean(self, value):
        if value == u'':
            return value

        for letter in value:
            if letter not in ALLOWED_SLUG_CHARS:
                raise forms.ValidationError(self.error_messages['invalid'])

        return value
