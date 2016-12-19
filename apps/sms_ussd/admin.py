# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import SMS

__author__ = 'AlexStarov'


class SendSMSAdmin(admin.ModelAdmin, ):
    pass

admin.site.register(SMS, SendSMSAdmin, )
