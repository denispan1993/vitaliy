# coding=utf-8
__author__ = 'Админ'

from django.contrib import admin

from applications.utils.captcha.models import Captcha_Images


class Captcha_Images_Admin(admin.ModelAdmin, ):
    pass
#    list_display = ['pk', 'order', 'is_active', 'parent', 'title', 'text', ]
#    list_display_links = ['pk', 'title', 'text', ]
#    fieldsets = [
#        (None, {'classes': ['wide'], 'fields': ['is_active', 'order', 'content_type', 'object_id',
#                                                'title', 'text', 'alt', 'slide', ], }),
#    ]
#    # readonly_fields = ('pk', )
admin.site.register(Captcha_Images, Captcha_Images_Admin, )

from applications.utils.captcha.models import Captcha_Key
admin.site.register(Captcha_Key, )
