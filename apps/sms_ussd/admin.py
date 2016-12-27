# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import SMS, Template, USSD

__author__ = 'AlexStarov'


class SMSAdmin(admin.ModelAdmin, ):
    list_display = ['pk', 'template', 'direction', 'user', 'sessionid', 'task_id',
                    'is_send', 'from_phone_char', 'to_phone_char', ]
    list_display_links = ['pk', 'direction', 'user', 'sessionid', 'task_id',
                          'is_send', 'from_phone_char', 'to_phone_char', ]

admin.site.register(SMS, SMSAdmin, )


class TemplateAdmin(admin.ModelAdmin, ):
    pass

admin.site.register(Template, TemplateAdmin, )


class USSDAdmin(admin.ModelAdmin, ):
    list_display = ['pk', 'from_device', 'direction', 'user', 'sessionid', 'task_id',
                    'is_send', 'from_phone_char', 'to_phone_char', ]
    list_display_links = ['pk', 'from_device', 'direction', 'user', 'sessionid', 'task_id',
                          'is_send', 'from_phone_char', 'to_phone_char', ]

admin.site.register(USSD, USSDAdmin, )
