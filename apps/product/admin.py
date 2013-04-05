# coding=utf-8
__author__ = 'Админ'

from django.contrib import admin

from apps.product.models import Photo
from django.contrib.contenttypes import generic
#from nested_inlines.admin import NestedModelAdmin, NestedStackedInline, NestedTabularInline


class GenericStacked_Photo_InLine(generic.GenericStackedInline, ): # generic.GenericStackedInline, NestedStackedInline,
    model = Photo
    extra = 2

from apps.product.models import Category


class CategoryAdmin(admin.ModelAdmin, ):
    list_display = ['pk', 'url', 'title', 'parent', 'name', ]
    list_display_links = ['pk', 'url', 'title', ]
    fieldsets = [
        (None,               {'classes': ['wide'], 'fields': ['parent', 'is_active', 'disclose_product', 'url',
                                                              'title', 'name', 'description', ], }),
        (u'Информация о категории для поисковых систем', {'classes': ['collapse'], 'fields': ['meta_title',
                                                                                              'meta_description',
                                                                                              'meta_keywords', ], }),
        (u'Дополнительные функции', {'classes': ['collapse'], 'fields': ['template', 'visibility', ], })
    ]
#    readonly_fields = (u'url', )
#    prepopulated_fields = {u'url' : (u'title',), }

#    prepopulated_fields = {'url' : ('title',), }

    inlines = [
        GenericStacked_Photo_InLine,
    ]
    save_as = True
    save_on_top = True

from apps.product.models import Information


class Stacked_Information_InLine(admin.TabularInline, ):
    model = Information
    extra = 3

from apps.product.models import Additional_Information


class Stacked_Additional_Information_InLine(admin.StackedInline, ):
    model = Additional_Information
    inlines = [
        Stacked_Information_InLine,
    ]
#    filter_horizontal = ('informations', )
#    filter_vertical = ('informations', )
    extra = 1


class Additional_Information_Admin(admin.ModelAdmin, ):
#    fieldsets = (
#                (None, {'fields': ('product', 'title', 'informations', )}),
#        )
#    filter_horizontal = ('informations', )
    inlines = [
        Stacked_Information_InLine,
    ]

from apps.product.models import Discount


class Tabular_Discount_InLine(admin.TabularInline, ):
    model = Discount
    extra = 3

from apps.product.models import Product
from django import forms


class ProductAdminForm(forms.ModelForm, ):
    class Meta:
        models = Product

from compat.ruslug import patch_admin_form


class ProductAdmin(admin.ModelAdmin, ):
    fieldsets = [
        (None,               {'classes': ['wide'], 'fields': ['category', 'is_active', 'disclose_product', 'url',
                                                              'title', 'name', 'description', 'minimal_quantity',
                                                              'weight', 'unit_of_measurement', 'regular_price',
                                                              'price', ], }),
        (u'Информация о товаре для поисковых систем', {'classes': ['collapse'], 'fields': ['meta_title',
                                                                                           'meta_description',
                                                                                           'meta_keywords', ], }),
        (u'Дополнительные функции', {'classes': ['collapse'], 'fields': ['template', 'visibility', ], })
    ]
#    readonly_fields = u'url'
    form = patch_admin_form(ProductAdminForm, )
    prepopulated_fields = {u'url' : (u'title',), }
    filter_horizontal = ('category', )

    inlines = [
        Tabular_Discount_InLine,
        Stacked_Additional_Information_InLine,
        GenericStacked_Photo_InLine,
    ]
    save_as = True
    save_on_top = True

from apps.product.models import Unit_of_Measurement


admin.site.register(Category, CategoryAdmin, )
admin.site.register(Product, ProductAdmin, )
admin.site.register(Additional_Information, Additional_Information_Admin, )
admin.site.register(Information, admin.ModelAdmin, )
admin.site.register(Unit_of_Measurement, admin.ModelAdmin, )
admin.site.register(Discount, admin.ModelAdmin, )
admin.site.register(Photo, admin.ModelAdmin, )
