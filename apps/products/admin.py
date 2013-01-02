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
        (None,               {'fields': ['parent', 'url', 'title', 'name', 'description', ]}),
        ('Meta information', {'fields': ['meta_title', 'meta_description', 'meta_keywords', ], 'classes': ['collapse']}),
        ('Additional information', {'fields': ['template', 'visibility', ], 'classes': ['collapse']})
    ]
    prepopulated_fields = {'url' : ('title',), }

    inlines = [
        PhotoInline,
    ]

class ProductAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['parent', 'url', 'title', 'name', 'description', ]}),
        ('Meta information', {'fields': ['meta_title', 'meta_description', 'meta_keywords', ], 'classes': ['collapse']}),
        ('Additional information', {'fields': ['template', 'visibility', ], 'classes': ['collapse']})
    ]
    prepopulated_fields = {'url' : ('title',), }

    inlines = [
        PhotoInline,
    ]

class PhotoAdmin(admin.ModelAdmin):
    pass

admin.site.register(Category, CategoryAdmin, )
admin.site.register(Product, ProductAdmin, )
admin.site.register(Photo, PhotoAdmin, )
