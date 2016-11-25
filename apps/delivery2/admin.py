# -*- coding: utf-8 -*-

from django.contrib import admin

from .models import Delivery, Message, EmailSubject, EmailTemplate, EmailImageTemplate

__author__ = 'AlexStarov'


class EmailSubjectInlineAdmin(admin.TabularInline, ):
    model = EmailSubject
    fields = ['subject', 'chance']
    extra = 1


class EmailTemplateInlineAdmin(admin.TabularInline, ):
    model = EmailTemplate
    fields = ['name', 'template', 'chance']
    extra = 1


class DeliveryAdmin(admin.ModelAdmin, ):
    list_display = ['pk', 'name', 'delivery_test', 'type', 'created_at', 'updated_at', ]
    list_display_links = ['pk', 'name', ]
    inlines = (EmailSubjectInlineAdmin, EmailTemplateInlineAdmin, )

    save_as = True
    save_on_top = True
    ordering = ['-created_at', ]


class MessageAdmin(admin.ModelAdmin, ):
    list_display = ['pk', 'delivery', 'is_send', 'email', 'created_at', 'updated_at', ]
    list_display_links = ['pk', 'delivery', ]

    save_as = True
    save_on_top = True
    ordering = ['-created_at', ]


class EmailImageInlineAdmin(admin.TabularInline, ):
    model = EmailImageTemplate
    fields = ['url', 'image']
    readonly_fields = ('url',)
    extra = 1

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = ['pk', 'delivery', 'name', 'chance', ]
    list_display_links = ['pk', 'delivery', 'name', 'chance', ]
    # TODO: Показ template письма в админ панеле.
    suit_form_includes = (
        ('delivery/admin/templates/iframe.html', 'middle', ''),
    )

    inlines = (EmailImageInlineAdmin, )

    save_as = True
    save_on_top = True
    ordering = ['-created_at', ]

admin.site.register(Delivery, DeliveryAdmin, )
admin.site.register(Message, MessageAdmin, )
admin.site.register(EmailTemplate, EmailTemplateAdmin, )
