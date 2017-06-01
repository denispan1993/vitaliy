# coding=utf-8
from django.contrib import admin

from .models import Cart, Order, Product, DeliveryCompany, Template

__author__ = 'AlexStarov'


class CartAdmin(admin.ModelAdmin, ):
    list_display = ['pk', 'user', 'sessionid', 'created_at', 'updated_at', ]
    list_display_links = ['pk', 'user', 'sessionid', ]
    search_fields = ('sessionid', )
admin.site.register(Cart, CartAdmin, )
#    list_display = ['pk', 'url', 'title', 'parent', 'name', ]
#    list_display_links = ['pk', 'url', 'title', ]
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


class OrderAdmin(admin.ModelAdmin, ):
    list_display = ['pk', 'user', 'sessionid', 'email', 'phone', 'created_at', 'updated_at', ]
    list_display_links = ['pk', 'user', 'sessionid', 'email', 'phone', ]
    search_fields = ('sessionid', 'email', 'phone', )
admin.site.register(Order, OrderAdmin, )


class ProductAdmin(admin.ModelAdmin, ):
    list_display = ['pk', 'object_id', 'product', 'quantity', 'price', 'created_at', 'updated_at', ]
    list_display_links = ['pk', 'object_id', 'product', 'quantity', 'price', ]
admin.site.register(Product, ProductAdmin, )


class DeliveryCompanyAdmin(admin.ModelAdmin, ):
    pass
admin.site.register(DeliveryCompany, DeliveryCompanyAdmin, )


class TemplateAdmin(admin.ModelAdmin, ):
    list_display = ['pk', 'name', 'is_system', 'created_at', 'updated_at', ]
    list_display_links = ['pk', 'name', 'is_system', 'created_at', 'updated_at', ]
admin.site.register(Template, TemplateAdmin, )
