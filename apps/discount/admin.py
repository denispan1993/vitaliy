# coding=utf-8
__author__ = 'Админ'

from django.contrib import admin


class ActionAdmin(admin.ModelAdmin, ):
    list_display = ['pk', 'name', 'datetime_start', 'datetime_end', 'auto_start',
                    'auto_end', 'auto_del', 'auto_del_action_from_product', 'auto_del_action_price', ]
    list_display_links = ['pk', 'name', 'datetime_start', 'datetime_end', ]
    list_filter = ('name', )
    search_fields = ['name', ]
    fieldsets = [
        (None,               {'classes': ['wide'], 'fields': ['name', 'datetime_start', 'datetime_end', 'auto_start',
                                                              'auto_end', 'auto_del', 'auto_del_action_from_product',
                                                              'auto_del_action_price', ], }, ),
#        (u'Информация о товаре для поисковых систем', {'classes': ['collapse'], 'fields': ['meta_title',
#                                                                                           'meta_description',
#                                                                                           'meta_keywords', ], }, ),
#        (u'Дополнительные функции', {'classes': ['collapse'], 'fields': ['template', 'visibility', ], }, ),
#        (u'Ссылка на пользователя создателя', {'classes': ['collapse'], 'fields': ['user_obj', ], }, ),
    ]
#    readonly_fields = u'url'
#    form = patch_admin_form(ProductAdminForm, )
#    prepopulated_fields = {u'url': (u'title', ), }
#    filter_horizontal = ('category', 'recommended', 'action', )
#    inlines = [
#        genericStacked_ItemID_InLine,
#        genericStacked_IntermediateModelManufacturer_InLine,
#        Tabular_Discount_InLine,
#        admin_Additional_Information_InLine,
#        genericStacked_Photo_InLine,
#        Tabular_AdditionalInformationForPrice_InLine,
#        Tabular_ExtendedPrice_InLine,
#    ]
    save_as = True
    save_on_top = True
    ordering = ['-created_at', ]

#    # Тут начинается магия, СуперАдмину показываем всё, а пользователю, показываем только его объекты
#    def queryset(self, request, ):
#        if request.user.is_superuser:
#            return super(ProductAdmin, self).queryset(request, )
#        else:
#            return super(ProductAdmin, self).queryset(request).filter(user_obj=request.user, )

#    # Так решим вторую задачу, в поле author подставляем request.user
#    def save_model(self, request, obj, form, change, ):
#        if getattr(obj, 'user_obj', None, ) is None:
#            obj.user_obj = request.user
#        obj.save()

#    class Media:
#        js = ('/media/js/admin/ruslug-urlify.js', )

from apps.discount.models import Action
admin.site.register(Action, ActionAdmin, )
