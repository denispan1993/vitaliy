# -*- coding: utf-8 -*-

from django.contrib import admin

from .models import Delivery, Message, EmailSubject, EmailTemplate, EmailImageTemplate, EmailUrlTemplate, MessageRedirectUrl

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


class MessageRedirectUrlAdmin(admin.ModelAdmin, ):
    list_display = ['pk', 'message', 'type', 'href', 'created_at', 'updated_at', ]
    list_display_links = ['pk', 'message', 'href', ]

    ordering = ['-created_at', ]


class MessageAdmin(admin.ModelAdmin, ):
    list_display = ['pk', 'delivery', 'is_send', 'email', 'created_at', 'updated_at', ]
    list_display_links = ['pk', 'delivery', ]

    save_as = True
    save_on_top = True
    ordering = ['-created_at', ]


class EmailImageTemplateAdmin(admin.ModelAdmin, ):
    list_display = ['pk', 'template', 'url', 'image', 'created_at', 'updated_at', ]
    list_display_links = ['pk', 'template', 'url', 'image', ]

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


class EmailUrlTemplateAdmin(admin.ModelAdmin, ):
    list_display = ['pk', 'template', 'href', 'created_at', 'updated_at', ]
    list_display_links = ['pk', 'template', 'href', ]

    ordering = ['-created_at', ]


class EmailUrlInlineAdmin(admin.TabularInline, ):

    model = EmailUrlTemplate
    fields = ['href', ]
    readonly_fields = ('href', )
    extra = 1

#    def has_add_permission(self, request):
#        return False

#    def has_delete_permission(self, request, obj=None):
#        return False


class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = ['pk', 'is_system', 'delivery', 'name', 'chance', ]
    list_display_links = ['pk', 'delivery', 'name', 'chance', ]
    # TODO: Показ template письма в админ панеле.
    suit_form_includes = (
        ('delivery/admin/templates/iframe.html', 'middle', ''),
    )

    inlines = (EmailImageInlineAdmin, EmailUrlInlineAdmin, )

    save_as = True
    save_on_top = True
    ordering = ['-created_at', ]

admin.site.register(Delivery, DeliveryAdmin, )
admin.site.register(MessageRedirectUrl, MessageRedirectUrlAdmin, )
admin.site.register(Message, MessageAdmin, )
admin.site.register(EmailImageTemplate, EmailImageTemplateAdmin, )
admin.site.register(EmailUrlTemplate, EmailUrlTemplateAdmin, )
admin.site.register(EmailTemplate, EmailTemplateAdmin, )
