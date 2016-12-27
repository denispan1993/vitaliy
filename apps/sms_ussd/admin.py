# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import SMS, Template

__author__ = 'AlexStarov'


class SMSAdmin(admin.ModelAdmin, ):
    list_display = ['pk', 'template', 'direction', 'user', 'sessionid', 'task-id',
                    'is_send', 'from_phone_char', 'to_phone_char', ]
    list_display_links = ['pk', 'direction', 'user', 'sessionid', 'task-id', ]

admin.site.register(SMS, SMSAdmin, )


class TemplateAdmin(admin.ModelAdmin, ):
    pass

admin.site.register(Template, TemplateAdmin, )
