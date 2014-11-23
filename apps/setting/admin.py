# coding=utf-8
__author__ = 'Админ'

from django.contrib import admin
from django.contrib.contenttypes import generic
from apps.product.models import Photo


class genericStacked_Photo_InLine(generic.GenericStackedInline, ):
    model = Photo
    extra = 1


from apps.setting.models import Setting


class SettingAdmin(admin.ModelAdmin, ):
    list_display = ['pk', 'name', 'variable_name', ]
    list_display_links = ['pk', 'name', 'variable_name', ]
    fieldsets = [
        (None, {'classes': ['wide'], 'fields': ['name', 'variable_name', 'variable', 'description', ], }),
    ]
    inlines = [
        genericStacked_Photo_InLine,
    ]

    # readonly_fields = ('pk', )

admin.site.register(Setting, SettingAdmin, )