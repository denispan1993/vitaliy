# -*- coding: utf-8 -*-
from django.contrib import admin

from apps.utils.mediafile.models import MediaFile
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext_lazy as _

from .models import MailServer, MailAccount, Email_Img, Delivery, Subject, EmailMiddleDelivery,\
    EmailForDelivery, SpamEmail, TraceOfVisits, RawEmail

__author__ = 'AlexStarov'


class MailServerAdmin(admin.ModelAdmin, ):
    list_display = ['pk', 'server_name', 'use_smtp', 'server_smtp', 'port_smtp', 'use_ssl_smtp', 'use_tls_smtp',
                    'use_imap', 'use_pop3',
                    'created_at', 'updated_at', ]
    list_display_links = ['pk', 'use_smtp', 'server_name', 'server_smtp', 'port_smtp', 'use_imap', 'use_pop3', ]

    fieldsets = [
        (None, {'classes': ['wide'], 'fields': ['server_name', 'use_smtp', 'server_smtp', 'port_smtp',
                                                'use_ssl_smtp', 'use_tls_smtp', ],
                },
         ),
        (_(u'IMAP'), {'classes': ['collapse'], 'fields': ['use_imap', 'server_imap', 'port_imap',
                                                          'use_ssl_imap', 'use_tls_imap', ],
                      },
         ),
        (_(u'POP3'), {'classes': ['collapse'], 'fields': ['use_pop3', 'server_pop3', 'port_pop3',
                                                          'use_ssl_pop3', 'use_tls_pop3', ],
                      },
         ),
        ]

admin.site.register(MailServer, MailServerAdmin, )


class MailAccountAdmin(admin.ModelAdmin, ):
    list_display = ['pk', 'use_smtp', 'is_auto_active', 'auto_active_datetime', 'email', 'username', 'created_at', 'updated_at', ]
    list_display_links = ['pk', 'email', 'username', ]
admin.site.register(MailAccount, MailAccountAdmin, )


class genericStackedMediaFileInLine(generic.GenericStackedInline, ):
    model = MediaFile
    extra = 1


class SubjectTabularInLine(admin.TabularInline, ):
    model = Subject
    extra = 1


class DeliveryAdmin(admin.ModelAdmin, ):
    list_display = ['pk', 'name', 'delivery_test', 'type', 'created_at', 'updated_at', ]
    list_display_links = ['pk', 'name', ]

    inlines = [
        SubjectTabularInLine, genericStackedMediaFileInLine,
    ]
    save_as = True
    save_on_top = True
    ordering = ['-created_at', ]

admin.site.register(Delivery, DeliveryAdmin, )


class EmailImgAdmin(admin.ModelAdmin, ):
    list_display = ['pk', 'name', 'tag_name', 'image', 'created_at', 'updated_at', ]
    list_display_links = ['pk', 'name', 'tag_name', ]
admin.site.register(Email_Img, EmailImgAdmin, )


class EmailMiddleDeliveryAdmin(admin.ModelAdmin, ):
    list_display = ['pk', 'delivery', 'delivery_test_send', 'delivery_send', 'created_at', 'updated_at', ]
    list_display_links = ['pk', 'delivery', ]
admin.site.register(EmailMiddleDelivery, EmailMiddleDeliveryAdmin, )


class EmailForDeliveryAdmin(admin.ModelAdmin, ):
    list_display = ['pk', 'delivery', 'key', 'send', 'created_at', ]
    list_display_links = ['pk', 'delivery', 'key', ]
admin.site.register(EmailForDelivery, EmailForDeliveryAdmin, )


class SpamEmailAdmin(admin.ModelAdmin, ):
    list_display = ['pk', 'email', 'bad_email', 'created_at', ]
    list_display_links = ['pk', 'email', 'created_at', ]

    search_fields = ['email', ]

    ordering = ['-created_at', ]

admin.site.register(SpamEmail, SpamEmailAdmin, )


class TraceOfVisitsAdmin(admin.ModelAdmin, ):
    list_display = ['pk', 'delivery', 'email_fk', 'sessionid', 'url',
                    'target', 'target_id', 'email_fk_key', 'created_at', ]
    list_display_links = ['pk', 'delivery', 'email_fk', 'email_fk_key', ]
    search_fields = ['url', ]

admin.site.register(TraceOfVisits, TraceOfVisitsAdmin, )


class RawEmailAdmin(admin.ModelAdmin, ):
    list_display = ['pk', 'message_id_header', 'from_header', 'to_header', 'subject_header', ]
    list_display_links = ['pk', 'message_id_header', 'from_header', 'to_header', 'subject_header', ]

admin.site.register(RawEmail, RawEmailAdmin, )

#class CouponAdmin(admin.ModelAdmin, ):
#    list_display = ['pk', 'name', 'coupon_group', 'key', 'number_of_possible_uses', 'number_of_uses', ]
#    list_display_links = ['pk', 'name', 'coupon_group', 'key', ]
#admin.site.register(Coupon, CouponAdmin, )
#    fieldsets = [
#        (None,               {'classes': ['wide'], 'fields': ['parent', 'is_active', 'disclose_product', 'url',
#                                                              'title', 'name', 'description', ], }),
#        (u'Информация о категории для поисковых систем', {'classes': ['collapse'], 'fields': ['meta_title',
#                                                                                              'meta_description',
#                                                                                              'meta_keywords', ], }),
#        (u'Дополнительные функции', {'classes': ['collapse'], 'fields': ['template', 'visibility', ], })
#    ]
#    readonly_fields = (u'url', )
#    prepopulated_fields = {u'url' : (u'title',), }

#    prepopulated_fields = {'url' : ('title',), }

#    inlines = [
#        GenericStacked_Photo_InLine,
#    ]
#    save_as = True
#    save_on_top = True

#    class Media:
#        js = ('/media/js/admin/ruslug-urlify.js', )

#from apps.cart.models import Order


#class OrderAdmin(admin.ModelAdmin, ):
#    list_display = ['pk', 'user', 'sessionid', 'email', 'phone', ]
#    list_display_links = ['pk', 'user', 'sessionid', 'email', 'phone', ]
#admin.site.register(Order, OrderAdmin, )

#from apps.cart.models import Product


#class ProductAdmin(admin.ModelAdmin, ):
#    list_display = ['pk', 'object_id', 'product', 'quantity', 'price', ]
#    list_display_links = ['pk', 'object_id', 'product', 'quantity', 'price', ]
#admin.site.register(Product, ProductAdmin, )
