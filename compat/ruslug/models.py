#! /usr/bin/env python
# -*- coding: utf-8 -*- 
from django.utils.translation import ugettext_lazy as _
from django.db import models
#import re

from compat.ruslug import forms


class RuSlugField(models.CharField):
    def formfield(self, **kwargs):
        defaults = {
            'form_class': forms.RuSlugFormField,
            'error_messages': {
                'invalid': _(u"Enter a valid 'slug' consisting of letters, numbers,"
                             u" underscores or hyphens."),
            }
        }
        defaults.update(kwargs)
        return super(RuSlugField, self).formfield(**defaults)
