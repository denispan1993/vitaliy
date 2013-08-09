# coding=utf-8
__author__ = 'Админ'

from django.contrib import admin

from apps.slide.models import Slide


class SlideAdmin(admin.ModelAdmin, ):
    list_display = ['pk', 'order', 'is_active', 'parent', 'title', 'text', ]
    list_display_links = ['pk', 'title', 'text', ]
    fieldsets = [
        (None, {'classes': ['wide'], 'fields': ['is_active', 'order', 'content_type', 'object_id',
                                                'title', 'text', 'alt', 'slide', ], }),
    ]
    # readonly_fields = ('pk', )

admin.site.register(Slide, SlideAdmin, )
