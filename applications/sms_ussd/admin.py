# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import SIM, SMS, Template, USSD

__author__ = 'AlexStarov'


class SIMAdmin(admin.ModelAdmin, ):
    list_display = ['imsi', 'name', 'phone', 'provider', ]
    list_display_links = ['imsi', 'name', 'phone', 'provider', ]

admin.site.register(SIM, SIMAdmin, )


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
    list_display = ['pk', 'direction', 'user', 'sessionid', 'task_id',
                    'is_send', ]
    list_display_links = ['pk', 'direction', 'user', 'sessionid', 'task_id',
                          'is_send', ]

admin.site.register(USSD, USSDAdmin, )
