# -*- coding: utf-8 -*-

from django.contrib import admin

from .models import Session_ID
from .models import HttpRequest_META


__author__ = 'AlexStarov'


#from apps.account.models import UserProfileModel


#class ProfileAdmin(admin.ModelAdmin, ):
#    pass
# admin.site.register(Profile, ProfileAdmin, )
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

@admin.register(Session_ID)
class Session_IDAdmin(admin.ModelAdmin, ):
    list_display = ('pk', 'user', 'sessionid', 'created_at', 'updated_at', )
    list_display_links = ('pk', 'user', 'sessionid', )
    search_fields = ['sessionid', ]

#from apps.account.models import UserProfileModel


#class UserProfileModelAdmin(admin.ModelAdmin, ):
#    pass
#admin.site.register(UserProfileModel, UserProfileModelAdmin, )


@admin.register(HttpRequest_META)
class HttpRequest_METAAdmin(admin.ModelAdmin, ):
    pass


#class OrderAdmin(admin.ModelAdmin, ):
#    list_display = ['pk', 'user', 'sessionid', 'email', 'phone', ]
#    list_display_links = ['pk', 'user', 'sessionid', 'email', 'phone', ]
#admin.site.register(Order, OrderAdmin, )

#from apps.cart.models import Product


#class ProductAdmin(admin.ModelAdmin, ):
#    list_display = ['pk', 'object_id', 'product', 'quantity', 'price', ]
#    list_display_links = ['pk', 'object_id', 'product', 'quantity', 'price', ]
#admin.site.register(Product, ProductAdmin, )
