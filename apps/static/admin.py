# coding=utf-8
__author__ = 'Админ'

from django.contrib import admin

from apps.static.models import Static


class StaticAdmin(admin.ModelAdmin, ):
    list_display = ['pk', 'order', 'url', 'title', ]
    list_display_links = ['pk', 'order', 'url', 'title', ]
    fieldsets = [
        (None, {'classes': ['wide'], 'fields': ['order', 'url', 'title', 'text', ], }, ),
        (u'Информация для поисковых систем', {'classes': ['collapse'], 'fields': ['meta_title', 'meta_description', 'meta_keywords', ], }, ),
        (u'Дополнительные функции', {'classes': ['collapse'], 'fields': ['template', 'visibility', ], })
    ]
    # readonly_fields = ('pk', )

    prepopulated_fields = {u'url': (u'title', ), u'meta_title': (u'title', ), }

admin.site.register(Static, StaticAdmin, )
