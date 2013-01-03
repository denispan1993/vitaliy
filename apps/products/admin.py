# coding=utf-8
__author__ = 'Админ'

from apps.products.models import Category, Product, Photo
from django.contrib import admin

from django.contrib.contenttypes import generic
class PhotoInline(generic.GenericTabularInline):
    model = Photo
    extra = 3

class CategoryAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'classes': ['wide'], 'fields': ['parent', 'url', 'title', 'name', 'description', ], }),
        ('Meta information', {'classes': ['collapse'], 'fields': ['meta_title', 'meta_description', 'meta_keywords', ], }),
        ('Additional information', {'classes': ['collapse'], 'fields': ['template', 'visibility', ], })
    ]
    prepopulated_fields = {'url' : ('title',), }

    inlines = [
        PhotoInline,
    ]

class ProductAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'classes': ['wide'], 'fields': ['category', 'url', 'title', 'name', 'description', ], }),
        ('Meta information', {'classes': ['collapse'], 'fields': ['meta_title', 'meta_description', 'meta_keywords', ], }),
        ('Additional information', {'classes': ['collapse'], 'fields': ['template', 'visibility', ], })
    ]
    prepopulated_fields = {'url' : ('title',), }
    filter_horizontal = ('category', )


    inlines = [
        PhotoInline,
    ]

class PhotoAdmin(admin.ModelAdmin):
    pass

admin.site.register(Category, CategoryAdmin, )
admin.site.register(Product, ProductAdmin, )
admin.site.register(Photo, PhotoAdmin, )
