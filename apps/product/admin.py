# coding=utf-8
__author__ = 'Админ'

from django.contrib import admin

from apps.product.models import Photo
from django.contrib.contenttypes import generic
from nested_inlines.admin import NestedModelAdmin, NestedStackedInline, NestedTabularInline


class genericStacked_Photo_InLine(generic.GenericStackedInline, ):
    model = Photo
    extra = 1

from apps.product.models import Category

from mptt.admin import MPTTModelAdmin


class CategoryAdmin(MPTTModelAdmin, ):
    #MPTT
    mptt_indent_field = 'url'
    #default is 10 pixels
    mptt_level_indent = 15

    list_display = ['pk', 'url', 'title', 'parent', ]  # 'name', ]
    list_display_links = ['pk', 'url', 'title', ]
    fieldsets = [
        (None,               {'classes': ['wide'], 'fields': ['parent', 'serial_number', 'is_active',
                                                              'shown_colored', 'shown_bold', 'shown_italic',
                                                              #'disclose_product',
                                                              'url', 'title',
                                                              #'letter_to_article',
                                                              # 'name',
                                                              'description', ], }),
        (u'Информация о категории для поисковых систем', {'classes': ['collapse'], 'fields': ['meta_title',
                                                                                              'meta_description',
                                                                                              'meta_keywords', ], }),
        (u'Дополнительные функции', {'classes': ['collapse'], 'fields': ['template', 'visibility', ], })
    ]
    #readonly_fields = (u'url', )
    prepopulated_fields = {'url': ('title', ), }

    inlines = [
        genericStacked_Photo_InLine,
    ]
    save_as = True
    save_on_top = True

    class Media:
        js = ('/media/js/admin/ruslug-urlify.js', )

from apps.product.models import ItemID


class ItemIDAdmin(admin.ModelAdmin, ):
    model = ItemID

    def save_model(*args, **kwargs):
        bbb = ItemID.bbb
        # pass

admin.site.register(ItemID, ItemIDAdmin, )


class genericStacked_ItemID_InLine(generic.GenericStackedInline, ):
    model = ItemID
    extra = 1
    max_num = 1

    def save_model(*args, **kwargs):
        bbb = ItemID.bbb
        # pass

from apps.product.models import IntermediateModelManufacturer


class genericStacked_IntermediateModelManufacturer_InLine(generic.GenericStackedInline, ):
    model = IntermediateModelManufacturer
    extra = 1
    max_num = 1

from apps.product.models import Manufacturer


class ManufacturerAdmin(admin.ModelAdmin, ):
    model = Manufacturer
admin.site.register(Manufacturer, ManufacturerAdmin, )


class generic_Photo_InLine_for_Information(generic.GenericStackedInline, ):
    model = Photo
    extra = 1
    max_num = 1

from apps.product.models import Information


class admin_Information_InLine(admin.TabularInline, ):
    model = Information
    inlines = [generic_Photo_InLine_for_Information, ]
    extra = 3

from apps.product.models import Additional_Information


class admin_Additional_Information_InLine(admin.StackedInline, ):
    model = Additional_Information
#    inlines = [
#        adminStacked_Information_InLine,
#    ]
#    filter_horizontal = ('informations', )
#    filter_vertical = ('informations', )
    extra = 5


#class NestedAdditional_Information_Admin(NestedModelAdmin, ): # admin.ModelAdmin
##    fieldsets = (
##                (None, {'fields': ('product', 'title', 'informations', )}),
##        )
##    filter_horizontal = ('informations', )
#    inlines = [
#        NestedStacked_Information_InLine,
#    ]

from apps.product.models import Discount


class Tabular_Discount_InLine(admin.TabularInline, ):
    model = Discount
    extra = 5

from apps.extended_price.models import Price_Additional_Information


class Tabular_Price_Additional_Information_InLine(admin.TabularInline, ):
    model = Price_Additional_Information
    extra = 3

from apps.extended_price.models import Price_Information


class Tabular_Price_Information_InLine(admin.TabularInline, ):
    model = Price_Information
    extra = 2

from apps.product.models import AdditionalInformationForPrice


class Tabular_AdditionalInformationForPrice_InLine(admin.TabularInline, ):
    model = AdditionalInformationForPrice
    filter_horizontal = ('information', )
    extra = 3

from apps.product.models import ExtendedPrice


class Tabular_ExtendedPrice_InLine(admin.TabularInline, ):
    model = ExtendedPrice
    filter_horizontal = ('information', )
    extra = 4

from apps.product.models import Product
#from django import forms


#class ProductAdminForm(forms.ModelForm, ):
#    class Meta:
#        models = Product


class ProductAdmin(admin.ModelAdmin, ):
    list_display = ['pk', 'url', 'title', 'name', ]
    list_display_links = ['pk', 'url', 'title', 'name', ]
    fieldsets = [
        (None,               {'classes': ['wide'], 'fields': ['category', 'is_active', 'disclose_product',
                                                              'in_main_page', 'url',
                                                              'title', 'name', 'description',  # 'manufacturer',
                                                              'recomendate',
                                                              'minimal_quantity',
                                                              'quantity_of_complete', 'weight', 'unit_of_measurement',
                                                              'is_availability', 'regular_price', 'price',
                                                              'price_of_quantity', ], }, ),
        (u'Информация о товаре для поисковых систем', {'classes': ['collapse'], 'fields': ['meta_title',
                                                                                           'meta_description',
                                                                                           'meta_keywords', ], }, ),
        (u'Дополнительные функции', {'classes': ['collapse'], 'fields': ['template', 'visibility', ], })
    ]
#    readonly_fields = u'url'
#    form = patch_admin_form(ProductAdminForm, )
    prepopulated_fields = {u'url': (u'title', ), }
    filter_horizontal = ('category', 'recomendate', )
    inlines = [
        genericStacked_ItemID_InLine,
        genericStacked_IntermediateModelManufacturer_InLine,
        Tabular_Discount_InLine,
        admin_Additional_Information_InLine,
        genericStacked_Photo_InLine,
        Tabular_AdditionalInformationForPrice_InLine,
        Tabular_ExtendedPrice_InLine,
    ]
    save_as = True
    save_on_top = True

    class Media:
        js = ('/media/js/admin/ruslug-urlify.js', )


from apps.product.models import Unit_of_Measurement

from apps.product.models import Country


class CountryAdmin(admin.ModelAdmin, ):
    list_display = ['pk', 'name_ru', 'name_en', 'phone_code', 'url', ]
    list_display_links = ['pk', 'name_ru', 'name_en', 'url', ]
    fieldsets = [
        (None,               {'classes': ['wide'], 'fields': ['name_ru', 'name_en', 'url', ], }, ),
    ]
    prepopulated_fields = {u'url': (u'name_ru', ), }

    save_as = True
    save_on_top = True

    class Media:
        js = ('/media/js/admin/ruslug-urlify.js', )

admin.site.register(Country, CountryAdmin, )
admin.site.register(Category, CategoryAdmin, )
admin.site.register(Product, ProductAdmin, )
#admin.site.register(Additional_Information, NestedAdditional_Information_Admin, )
admin.site.register(Information, admin.ModelAdmin, )
admin.site.register(Unit_of_Measurement, admin.ModelAdmin, )
admin.site.register(Discount, admin.ModelAdmin, )
admin.site.register(Photo, admin.ModelAdmin, )

from apps.product.models import View
admin.site.register(View, admin.ModelAdmin, )
from apps.product.models import Viewed
admin.site.register(Viewed, admin.ModelAdmin, )
#from apps.product.models import ExtendedPrice
#admin.site.register(ExtendedPrice, admin.ModelAdmin, )
from apps.product.models import InformationForPrice
admin.site.register(InformationForPrice, admin.ModelAdmin, )
