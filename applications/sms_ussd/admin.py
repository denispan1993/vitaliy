# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import SIM, SMS, Template, USSD

__author__ = 'AlexStarov'


@admin.register(SIM)
class SIMAdmin(admin.ModelAdmin, ):
    list_display = ['imsi', 'name', 'phone', 'provider', ]
    list_display_links = ['imsi', 'name', 'phone', 'provider', ]


@admin.register(SMS)
class SMSAdmin(admin.ModelAdmin, ):
    list_display = ['pk', 'template', 'direction', 'user', 'sessionid', 'task_id',
                    'is_send', 'from_phone_char', 'to_phone_char', 'created_at', 'updated_at', ]
    list_display_links = ['pk', 'direction', 'user', 'sessionid', 'task_id',
                          'is_send', 'from_phone_char', 'to_phone_char', ]
    list_filter = ('template', 'direction', 'user', 'is_send', 'from_phone_char', 'to_phone_char', )
    ordering = ['created_at', ]


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin, ):
    pass


@admin.register(USSD)
class USSDAdmin(admin.ModelAdmin, ):
    list_display = ['pk', 'direction', 'user', 'sessionid', 'task_id',
                    'is_send', ]
    list_display_links = ['pk', 'direction', 'user', 'sessionid', 'task_id',
                          'is_send', ]
