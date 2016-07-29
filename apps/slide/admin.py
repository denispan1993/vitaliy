# -*- coding: utf-8 -*-
from django.contrib import admin
from apps.slide.models import Slide

__author__ = 'AlexStarov'


class SlideAdmin(admin.ModelAdmin, ):
    list_display = ['pk', 'order', 'is_active', 'parent', 'title', 'text', ]
    list_display_links = ['pk', 'title', 'text', ]
    fieldsets = [
        (None, {'classes': ['wide'], 'fields': ['is_active', 'order', 'url', 'opening_method', 'content_type',
                                                'object_id', 'title', 'text', 'alt', 'slide', ], }),
    ]

admin.site.register(Slide, SlideAdmin, )
