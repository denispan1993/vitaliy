# coding=utf-8
__author__ = 'Alex Starov'

from django.contrib import admin


from apps.extended_price.models import Price_Additional_Information


class Price_Additional_Information_Admin(admin.ModelAdmin, ):
    pass

admin.site.register(Price_Additional_Information, Price_Additional_Information_Admin, )

from apps.extended_price.models import Price_Information


class Price_Information_Admin(admin.ModelAdmin, ):
    pass

admin.site.register(Price_Information, Price_Information_Admin, )

from apps.extended_price.models import Extended_Price


class Extended_Price_Admin(admin.ModelAdmin, ):
    pass

admin.site.register(Extended_Price, Extended_Price_Admin, )
