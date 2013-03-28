# coding=utf-8
__author__ = 'Админ'

from django.contrib import admin

from apps.product.models import Photo
from django.contrib.contenttypes import generic


class PhotoInLine(generic.GenericTabularInline):
    model = Photo
    extra = 1

from apps.product.models import Category


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['pk', 'url', 'title', 'parent', 'name', ]
    list_display_links = ['pk', 'url', 'title', ]
    fieldsets = [
        (None,               {'classes': ['wide'], 'fields': ['parent', 'url', 'title', 'name', 'description', ], }),
        ('Meta information', {'classes': ['collapse'], 'fields': ['meta_title', 'meta_description', 'meta_keywords', ], }),
        ('Additional information', {'classes': ['collapse'], 'fields': ['template', 'visibility', ], })
    ]
#    readonly_fields = (u'url', )
    prepopulated_fields = {u'url' : (u'title',), }

#    prepopulated_fields = {'url' : ('title',), }

    inlines = [
        PhotoInLine,
    ]
    save_as = True
    save_on_top = True

from apps.product.models import Information


class InformationInLine(admin.TabularInline):
    model = Information
    extra = 5

from apps.product.models import Additional_Information


class Additional_InformationAdmin(admin.ModelAdmin):
    inlines = [
        InformationInLine,
    ]


class Additional_InformationInLine(admin.StackedInline):
    model = Additional_Information
    inlines = [
        InformationInLine,
    ]
    extra = 1

from apps.product.models import Discount


class DiscountInLine(admin.TabularInline):
    model = Discount
    extra = 5

from apps.product.models import Product


class ProductAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'classes': ['wide'], 'fields': ['category', 'url', 'title', 'name', 'description', 'regular_price', 'price', ], }),
        ('Meta information', {'classes': ['collapse'], 'fields': ['meta_title', 'meta_description', 'meta_keywords', ], }),
        ('Additional information', {'classes': ['collapse'], 'fields': ['template', 'visibility', ], })
    ]
#    readonly_fields = u'url'
#    prepopulated_fields = {u'url' : (u'title',), }
    filter_horizontal = ('category', )

    inlines = [
        # InformationInLine,
        Additional_InformationInLine,
#        PhotoInLine,
#        DiscountInLine,
    ]
    save_as = True
    save_on_top = True


class InformationAdmin(admin.ModelAdmin):
    pass

from apps.product.models import Unit_of_Measurement


class Unit_of_MeasurementAdmin(admin.ModelAdmin):
    pass


class DiscountAdmin(admin.ModelAdmin):
    pass


class PhotoAdmin(admin.ModelAdmin):
    pass

admin.site.register(Category, CategoryAdmin, )
admin.site.register(Product, ProductAdmin, )
admin.site.register(Additional_Information, Additional_InformationAdmin, )
admin.site.register(Information, InformationAdmin, )
admin.site.register(Unit_of_Measurement, Unit_of_MeasurementAdmin, )
admin.site.register(Discount, DiscountAdmin, )
admin.site.register(Photo, PhotoAdmin, )
