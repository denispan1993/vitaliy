# -*- coding: utf-8 -*-

from apps.product.models import Manufacturer
from django.contrib import admin
from django.contrib.contenttypes import generic

from mptt.admin import MPTTModelAdmin

from .models import Category, Photo, ItemID, IntermediateModelManufacturer, Information, Additional_Information

admin.site.register(Photo, admin.ModelAdmin, )

#from nested_inlines.admin import NestedModelAdmin, NestedStackedInline, NestedTabularInline

__author__ = 'AlexStarov'


class genericStackedPhotoInLine(generic.GenericStackedInline, ):
    model = Photo
    extra = 1


class CategoryAdmin(MPTTModelAdmin, ):
    #MPTT
    mptt_indent_field = 'url'
    #default is 10 pixels
    mptt_level_indent = 15

    list_display = ('pk', 'url', 'title', 'parent', )  # 'name', ]
    list_display_links = ('pk', 'url', 'title', )
    list_filter = ('title', )
    search_fields = ['title', ]
    fieldsets = [
        (None,   {'classes': ['wide'], 'fields': ['parent', 'serial_number', 'is_active',
                                                  'shown_colored', 'font_color',
                                                  'shadow_color', 'shadow_px', 'shadow_blur_px',
                                                  'shown_bold', 'shown_italic', 'font_px',
                                                  'url', 'title',
                                                  'item_description', 'description', ], }),
        (u'Информация о категории для поисковых систем', {'classes': ['collapse'], 'fields': ['meta_title',
                                                                                              'meta_description',
                                                                                              'meta_keywords', ], }, ),
        (u'Дополнительные функции', {'classes': ['collapse'], 'fields': ['template', 'visibility', ], }, ),
        (u'Ссылка на пользователя создателя', {'classes': ['collapse'], 'fields': ['user_obj', ], }, ),
    ]

    prepopulated_fields = {'url': ('title', ), }

    inlines = [
        genericStackedPhotoInLine,
    ]
    save_as = True
    save_on_top = True
    ordering = ['-created_at', ]

    # В поле author подставляем request.user
    def save_model(self, request, obj, form, change):
        if getattr(obj, 'user_obj', None, ) is None:
            obj.user_obj = request.user
        obj.save()

    class Media:
        js = ('/media/js/admin/ruslug-urlify.js', )


class ItemIDAdmin(admin.ModelAdmin, ):
    model = ItemID

    def save_model(*args, **kwargs):
        bbb = ItemID.bbb
        # pass

admin.site.register(ItemID, ItemIDAdmin, )


class genericStackedItemIDInLine(generic.GenericStackedInline, ):
    model = ItemID
    extra = 1
    max_num = 1

    def save_model(*args, **kwargs):
        bbb = ItemID.bbb
        # pass


class genericStacked_IntermediateModelManufacturer_InLine(generic.GenericStackedInline, ):
    model = IntermediateModelManufacturer
    extra = 1
    max_num = 1


class ManufacturerAdmin(admin.ModelAdmin, ):
    model = Manufacturer
admin.site.register(Manufacturer, ManufacturerAdmin, )


class genericPhotoInLineforInformation(generic.GenericStackedInline, ):
    model = Photo
    extra = 1
    max_num = 1


class admin_Information_InLine(admin.TabularInline, ):
    model = Information
    inlines = [genericPhotoInLineforInformation, ]
    extra = 3


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

#from apps.extended_price.models import Price_Additional_Information


#class Tabular_Price_Additional_Information_InLine(admin.TabularInline, ):
#    model = Price_Additional_Information
#    extra = 3

#from apps.extended_price.models import Price_Information


#class Tabular_Price_Information_InLine(admin.TabularInline, ):
#    model = Price_Information
#    extra = 2

#from apps.product.models import AdditionalInformationAndInformationForPrice


#class Tabular_AdditionalInformationAndInformationForPrice_InLine(admin.TabularInline, ):
#    model = AdditionalInformationAndInformationForPrice

from apps.product.models import AdditionalInformationForPrice


class Tabular_AdditionalInformationForPrice_InLine(admin.TabularInline, ):
    model = AdditionalInformationForPrice
#    inlines = (Tabular_AdditionalInformationAndInformationForPrice_InLine, )
    filter_horizontal = ('information', )
    extra = 3

# from django import forms
from apps.product.models import ExtendedPrice


# class ExtendedPriceForm(forms.ModelForm):
#     class Meta:
#         model = ExtendedPrice
#         widgets = {
#             'information': forms.SelectMultiple(attrs={'product': 1, }, ),
#         }


class Tabular_ExtendedPrice_InLine(admin.TabularInline, ):
    model = ExtendedPrice
    # form = ExtendedPriceForm
    filter_horizontal = ('information', )
    extra = 4

    def get_formset(self, request, obj=None, **kwargs):
        # Save parent instance
        self.obj = obj
        return super(Tabular_ExtendedPrice_InLine, self).get_formset(request, obj, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "information":
#            obj = self.obj
#            id = request.path.split('/')[-2]
#            if id:
#                try:
#                    id = int(id)
#                except ValueError:
#                    pass
#                else:
#                    from apps.product.models import Product
#                    product = Product.objects.get(pk=id, )
##                    aaa123
#                    from apps.product.models import InformationForPrice
#                    from django.db.models import Q
#                    kwargs["queryset"] =\
#                        InformationForPrice.objects.filter(Q(product=product, ) | Q(product__isnull=True, ), )
            from apps.product.models import InformationForPrice
            from django.db.models import Q
            kwargs["queryset"] =\
                InformationForPrice.objects.filter(Q(product=self.obj, ) | Q(product__isnull=True, ), )
        return super(Tabular_ExtendedPrice_InLine, self).formfield_for_manytomany(db_field, request, **kwargs)

    # def get_formset(self, request, obj=None, **kwargs):
    #     # Save parent instance
    #     self.obj = obj
    #     return super(Tabular_ExtendedPrice_InLine, self).get_formset(request, obj, **kwargs)

    # def formfield_for_dbfield(self, db_field, **kwargs):
    #     field = super(Tabular_ExtendedPrice_InLine, self).formfield_for_dbfield(db_field, **kwargs)
    #     if db_field.name == 'information' and hasattr(self, 'obj') and self.obj:
    #         # field.choices = [('','---------')]
    #         # field.choices.extend(Column.objects.filter(table=self.obj.table).values_list('id', 'title'))
    #     # return field

    # def queryset(self, request, ):
    #     qs = super(ExtendedPrice, self, ).queryset(request, )
    #     if request.user.is_superuser:
    #         return qs
    #     return qs.filter(author=request.user)

from apps.product.models import Product


from django import forms


class ProductAdminForm(forms.ModelForm):

    class Meta:
        models = Product
        from django.forms import widgets
        from suit_ckeditor.widgets import CKEditorWidget
        from suit.widgets import AutosizedTextarea
        widgets = {# 'name': widgets.TextInput(attrs={'size': 63, }, ),
                   # 'title': widgets.TextInput(attrs={'size': 63, }, ),
                   'name': AutosizedTextarea(attrs={'class': 'input-xxlarge', }, ),  # 'class': 'input-xlarge', 'style': 'with:500px;',
                   'title': AutosizedTextarea(attrs={'class': 'input-xxlarge', }, ),
                   # You can also specify html attributes
                   # 'description': AutosizedTextarea(attrs={'rows': 3, 'class': 'input-xlarge'}),
                   # 'item_description': CKEditorWidget(editor_options={'startupFocus': False, }, ),
                   'description': CKEditorWidget(editor_options={'startupFocus': False, }, ),
                   }


class ProductAdmin(admin.ModelAdmin, ):
    list_display = ['pk', 'url', 'title', 'name', ]
    list_display_links = ['pk', 'url', 'title', 'name', ]
    list_filter = ('title', 'name', )
    search_fields = ['title', 'name', ]
    form = ProductAdminForm
    fieldsets = [
        (None,               {'classes': ['wide'], 'fields': ['category', 'is_active', 'disclose_product',
                                                              'in_main_page', 'serial_number', 'url',
                                                              'title', 'name', 'description',  # 'manufacturer',
                                                              'recommended',
                                                              'minimal_quantity',
                                                              'quantity_of_complete', 'weight', 'unit_of_measurement',
                                                              'is_availability', 'regular_price', 'currency',
                                                              'price', 'price_of_quantity',
                                                              'action', 'action_price', ], }, ),
        (u'Информация о товаре для поисковых систем', {'classes': ['collapse'], 'fields': ['meta_title',
                                                                                           'meta_description',
                                                                                           'meta_keywords', ], }, ),
        (u'Дополнительные функции', {'classes': ['collapse'], 'fields': ['template', 'visibility', ], }, ),
        (u'Ссылка на пользователя создателя', {'classes': ['collapse'], 'fields': ['user_obj', ], }, ),
    ]
#    readonly_fields = u'url'
#    form = patch_admin_form(ProductAdminForm, )
    prepopulated_fields = {u'url': (u'title', ), }
    filter_horizontal = ('category', 'recommended', 'action', )
    inlines = [
        genericStackedItemIDInLine,
        genericStacked_IntermediateModelManufacturer_InLine,
        Tabular_Discount_InLine,
        admin_Additional_Information_InLine,
        genericStackedPhotoInLine,
        Tabular_AdditionalInformationForPrice_InLine,
        Tabular_ExtendedPrice_InLine,
    ]
    save_as = True
    save_on_top = True
    ordering = ['-created_at', ]

    # Тут начинается магия, СуперАдмину показываем всё, а пользователю, показываем только его объекты
    # def queryset(self, request, ):
    #     if request.user.is_superuser:
    #         return super(ProductAdmin, self).queryset(request, )
    #     else:
    #         return super(ProductAdmin, self).queryset(request).filter(user_obj=request.user, )

    # Так решим вторую задачу, в поле author подставляем request.user
    def save_model(self, request, obj, form, change, ):
        if getattr(obj, 'user_obj', None, ) is None:
            obj.user_obj = request.user
        obj.save()

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

from apps.product.models import Region


class RegionAdmin(admin.ModelAdmin, ):
    list_display = ['pk', 'name_ru', 'name_en', 'url', ]
    list_display_links = ['pk', 'name_ru', 'name_en', 'url', ]
    search_fields = ['name_ru', ]

    fieldsets = [
        (None,               {'classes': ['wide'], 'fields': ['country', 'name_ru', 'name_en', 'url', ], }, ),
    ]
    prepopulated_fields = {u'url': (u'name_ru', ), }

    save_as = True
    save_on_top = True

    class Media:
        js = ('/media/js/admin/ruslug-urlify.js', )

admin.site.register(Region, RegionAdmin, )

from apps.product.models import City


class CityAdmin(admin.ModelAdmin, ):
    list_display = ['pk', 'name_ru', 'name_en', 'phone_code', 'url', ]
    list_display_links = ['pk', 'name_ru', 'name_en', 'url', ]
    search_fields = ['name_ru', ]

    fieldsets = [
        (None,               {'classes': ['wide'], 'fields': ['region', 'name_ru', 'name_en',
                                                              'phone_code', 'url', ], }, ),
    ]
    prepopulated_fields = {u'url': (u'name_ru', ), }

    save_as = True
    save_on_top = True

    class Media:
        js = ('/media/js/admin/ruslug-urlify.js', )

admin.site.register(City, CityAdmin, )

from apps.product.models import Currency


class CurrenceAdmin(admin.ModelAdmin, ):
    list_display = ['pk', 'country', 'name_ru', 'name_truncated', 'name_en', ]
    list_display_links = ['pk', 'name_ru', 'name_truncated', 'name_en', ]
    fieldsets = [
        (None,               {'classes': ['wide'], 'fields': ['country', 'name_ru', 'name_truncated',
                                                              'name_en', 'currency', 'exchange_rate', ], }, ),
    ]

admin.site.register(Currency, CurrenceAdmin, )

admin.site.register(Category, CategoryAdmin, )
admin.site.register(Product, ProductAdmin, )
#admin.site.register(Additional_Information, NestedAdditional_Information_Admin, )
admin.site.register(Information, admin.ModelAdmin, )
admin.site.register(Unit_of_Measurement, admin.ModelAdmin, )
admin.site.register(Discount, admin.ModelAdmin, )

from apps.product.models import View
admin.site.register(View, admin.ModelAdmin, )
from apps.product.models import Viewed
admin.site.register(Viewed, admin.ModelAdmin, )
#from apps.product.models import ExtendedPrice
#admin.site.register(ExtendedPrice, admin.ModelAdmin, )
from apps.product.models import InformationForPrice


class InformationForPriceAdmin(admin.ModelAdmin, ):
    list_display = ['pk', 'information', ]
    list_display_links = ['pk', 'information', ]
    fieldsets = [
        (None,               {'classes': ['wide'], 'fields': ['product', 'information', ], }, ),
    ]
    readonly_fields = ('product', )
admin.site.register(InformationForPrice, InformationForPriceAdmin, )
