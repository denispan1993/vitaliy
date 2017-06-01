# -*- coding: utf-8 -*-
# /applications/utils/setting/admin.py
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericStackedInline

from applications.product.models import Photo
from .models import Setting

__author__ = 'AlexStarov'


class genericStacked_Img_InLine(GenericStackedInline, ):
    model = Photo
    extra = 1


class SettingAdmin(admin.ModelAdmin, ):
    list_display = ['pk', 'name', 'variable_name', ]
    list_display_links = ['pk', 'name', 'variable_name', ]
    fieldsets = [
        (None, {'classes': ['wide'], 'fields': ['name', 'variable_name', 'description',
                                                'char', 'text',
                                                'positivesmallinteger', ], }),
    ]
    inlines = [
        genericStacked_Img_InLine,
    ]

    # readonly_fields = ('pk', )

admin.site.register(Setting, SettingAdmin, )
