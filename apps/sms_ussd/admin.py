# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import SMS, Template

__author__ = 'AlexStarov'


class SMSAdmin(admin.ModelAdmin, ):
    pass

admin.site.register(SMS, SMSAdmin, )


class TemplateAdmin(admin.ModelAdmin, ):
    pass

admin.site.register(Template, TemplateAdmin, )
