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
        (None,       {'classes': ['wide'], 'fields': ['parent', 'serial_number', 'is_active',
                                                      'shown_colored', 'shown_bold', 'shown_italic', 'font_px',
                                                      #'disclose_product',
                                                      'url', 'title',
                                                      #'letter_to_article',
                                                      # 'name',
                                                      'item_description', 'description', ], }),
        (u'Информация о категории для поисковых систем', {'classes': ['collapse'], 'fields': ['meta_title',
                                                                                              'meta_description',
                                                                                              'meta_keywords', ], }, ),
        (u'Дополнительные функции', {'classes': ['collapse'], 'fields': ['template', 'visibility', ], }, ),
        (u'Ссылка на пользователя создателя', {'classes': ['collapse'], 'fields': ['user_obj', ], }, ),
    ]
    #readonly_fields = (u'url', )
    prepopulated_fields = {'url': ('title', ), }

    inlines = [
        genericStacked_Photo_InLine,
    ]
    save_as = True
    save_on_top = True
    ordering = ['-created_at', ]

    # В поле author подставляем request.user
    def save_model(self, request, obj, form, change):
        if getattr(obj, 'user_obj', None, ) is None:
            obj.author = request.user
        obj.save()

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
#from django import forms


#class ProductAdminForm(forms.ModelForm, ):
#    class Meta:
#        models = Product


class ProductAdmin(admin.ModelAdmin, ):
    list_display = ['pk', 'url', 'title', 'name', ]
    list_display_links = ['pk', 'url', 'title', 'name', ]
    fieldsets = [
        (None,               {'classes': ['wide'], 'fields': ['category', 'is_active', 'disclose_product',
                                                              'in_main_page', 'serial_number', 'url',
                                                              'title', 'name', 'description',  # 'manufacturer',
                                                              'recomendate',
                                                              'minimal_quantity',
                                                              'quantity_of_complete', 'weight', 'unit_of_measurement',
                                                              'is_availability', 'regular_price', 'price',
                                                              'price_of_quantity', ], }, ),
        (u'Информация о товаре для поисковых систем', {'classes': ['collapse'], 'fields': ['meta_title',
                                                                                           'meta_description',
                                                                                           'meta_keywords', ], }, ),
        (u'Дополнительные функции', {'classes': ['collapse'], 'fields': ['template', 'visibility', ], }, ),
        (u'Ссылка на пользователя создателя', {'classes': ['collapse'], 'fields': ['user_obj', ], }, ),
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
    ordering = ['-created_at', ]

    # Тут начинается магия, СуперАдмину показываем всё, а пользователю, показываем только его объекты
    def queryset(self, request, ):
        if request.user.is_superuser:
            return super(ProductAdmin, self).queryset(request, )
        else:
            return super(ProductAdmin, self).queryset(request).filter(author=request.user, )

    # Так решим вторую задачу, в поле author подставляем request.user
    def save_model(self, request, obj, form, change):
        if getattr(obj, 'user_obj', None, ) is None:
            obj.author = request.user
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


class InformationForPriceAdmin(admin.ModelAdmin, ):
    list_display = ['pk', 'information', ]
    list_display_links = ['pk', 'information', ]
    fieldsets = [
        (None,               {'classes': ['wide'], 'fields': ['product', 'information', ], }, ),
    ]
    readonly_fields = ('product', )
admin.site.register(InformationForPrice, InformationForPriceAdmin, )
