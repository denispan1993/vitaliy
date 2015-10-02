# -*- coding: utf-8 -*-
__author__ = 'AlexStarov'

from django.contrib import admin

from apps.utils.mediafile.models import MediaFile
from django.contrib.contenttypes import generic

from apps.delivery.models import MailAccount


class MailAccountAdmin(admin.ModelAdmin, ):
    list_display = ['pk', 'email', 'smtp_server', 'smtp_port', 'login', 'created_at', 'updated_at', ]
    list_display_links = ['pk', 'email', 'login', ]
admin.site.register(MailAccount, MailAccountAdmin, )


class genericStacked_MediaFile_InLine(generic.GenericStackedInline, ):
    model = MediaFile
    extra = 1

from apps.delivery.models import Delivery


class DeliveryAdmin(admin.ModelAdmin, ):
    list_display = ['pk', 'name', 'delivery_test', 'type', 'subject', 'created_at', 'updated_at', ]
    list_display_links = ['pk', 'name', 'subject', ]

    inlines = [
        genericStacked_MediaFile_InLine,
    ]
    save_as = True
    save_on_top = True
    ordering = ['-created_at', ]

admin.site.register(Delivery, DeliveryAdmin, )


from apps.delivery.models import EmailMiddleDelivery


class EmailMiddleDeliveryAdmin(admin.ModelAdmin, ):
    list_display = ['pk', 'delivery', 'delivery_test_send', 'delivery_send', 'created_at', 'updated_at', ]
    list_display_links = ['pk', 'delivery', ]
admin.site.register(EmailMiddleDelivery, EmailMiddleDeliveryAdmin, )




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
