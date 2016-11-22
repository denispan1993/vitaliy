# -*- coding: utf-8 -*-

from django.contrib import admin

from .models import Delivery, Message

__author__ = 'AlexStarov'


class DeliveryAdmin(admin.ModelAdmin, ):
    list_display = ['pk', 'name', 'delivery_test', 'type', 'created_at', 'updated_at', ]
    list_display_links = ['pk', 'name', ]

    save_as = True
    save_on_top = True
    ordering = ['-created_at', ]


class MessageAdmin(admin.ModelAdmin, ):
    list_display = ['pk', 'delivery', 'is_send', 'email', 'created_at', 'updated_at', ]
    list_display_links = ['pk', 'delivery', ]

    save_as = True
    save_on_top = True
    ordering = ['-created_at', ]

admin.site.register(Delivery, DeliveryAdmin, )
admin.site.register(Message, MessageAdmin, )
