# -*- coding: utf-8 -*-
from django.contrib import admin
from django.db.models import Q
from datetime import timedelta
from django import forms

from django.contrib.contenttypes.models import ContentType
from .models import Slide

__author__ = 'AlexStarov'


class FilterModelForm(forms.ModelForm):
    class Meta:
        model = Slide
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        forms.ModelForm.__init__(self, *args, **kwargs)
        # coupon = kwargs.get('instance')
        # print(coupon)
        #print(coupon.start_of_the_coupon, )
        #print(timedelta(days=31), )
        #print(coupon.start_of_the_coupon - timedelta(days=31), )
        #print(coupon.end_of_the_coupon, timedelta(days=31), coupon.end_of_the_coupon + timedelta(days=31))
#        q = Q(created_at__gte=coupon.start_of_the_coupon - timedelta(days=5),
#              created_at__lte=coupon.end_of_the_coupon + timedelta(days=5),) |\
#            Q(updated_at__gte=coupon.start_of_the_coupon - timedelta(days=5),
#              updated_at__lte=coupon.end_of_the_coupon + timedelta(days=5), )

        # print(self.fields['content_type'].queryset)
        # for field in self.fields['content_type'].queryset:
        #     print(field.pk, field.app_label, ' : ', field.model)

        '''
            (9L, u'static', ' : ', u'static')
            (11L, u'product', ' : ', u'category')
            (12L, u'product', ' : ', u'product')
        '''
        self.fields['content_type'].queryset = ContentType.objects.filter(pk__in=[9, 11, 12, ])
        #self.fields['content_type'].queryset = Cart.objects.filter(q).order_by('updated_at', )
        #self.fields['child_cart'].queryset = Cart.objects.all().order_by('updated_at', )
        # print(len(self.fields['child_cart'], ), self.fields['child_cart'].first().created_at, self.fields['child_cart'].last().created_at, )

        #self.fields['child_order'].queryset = Order.objects.filter(q).order_by('updated_at', )
        #self.fields['child_order'].queryset = Order.objects.all().order_by('updated_at', )
        # print(len(self.fields['child_order'], ), self.fields['child_order'].first().created_at, self.fields['child_order'].last().created_at, )
        # for key, value in kwargs.items():
        #     print('key: ', key, ' value: ', value, )


@admin.register(Slide)
class SlideAdmin(admin.ModelAdmin, ):
    list_display = ['pk', 'order', 'is_active', 'parent', 'title', 'text', ]
    list_display_links = ['pk', 'title', 'text', ]
    form = FilterModelForm

    fieldsets = [
        (None, {'classes': ['wide'], 'fields': ['is_active', 'order', 'url', 'opening_method', 'content_type',
                                                'object_id', 'title', 'text', 'alt', 'slide', ], }),
    ]
