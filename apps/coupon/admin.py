# -*- coding: utf-8 -*-

from django import forms
from django.contrib import admin
from django.db.models import Q
from datetime import timedelta

from .models import CouponGroup, Coupon
from apps.cart.models import Cart, Order

__author__ = 'AlexStarov'


@admin.register(CouponGroup)
class CouponGroupAdmin(admin.ModelAdmin, ):
    pass
#admin.site.register(CouponGroup, CouponGroupAdmin, )


class FilterModelForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        forms.ModelForm.__init__(self, *args, **kwargs)
        coupon = kwargs.get('instance')
        print(coupon.start_of_the_coupon, )
        print(timedelta(days=31), )
        print(coupon.start_of_the_coupon - timedelta(days=31), )
        print(coupon.end_of_the_coupon, timedelta(days=31), coupon.end_of_the_coupon + timedelta(days=31))
        q = Q(created_at__gte=coupon.start_of_the_coupon - timedelta(days=31),
              created_at__lte=coupon.end_of_the_coupon + timedelta(days=31),) |\
            Q(updated_at__gte=coupon.start_of_the_coupon - timedelta(days=31),
              updated_at__lte=coupon.end_of_the_coupon + timedelta(days=31), )

        self.fields['child_cart'].queryset = Cart.objects.filter(q).order_by('updated_at', )
        print(len(self.fields['child_cart'], ), )
        self.fields['child_order'].queryset = Order.objects.filter(q).order_by('updated_at', )
        print(len(self.fields['child_order'], ), )
        for key, value in kwargs.items():
            print('key: ', key, ' value: ', value, )


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin, ):
    form = FilterModelForm
    list_display = ['pk', 'name', 'coupon_group', 'key', 'number_of_possible_uses', 'number_of_uses', ]
    list_display_links = ['pk', 'name', 'coupon_group', 'key', ]

    filter_horizontal = ('child_cart', 'child_order', )

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
