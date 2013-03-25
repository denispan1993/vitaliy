# coding=utf-8
__author__ = 'Админ'

#from django.contrib import admin
#from apps.account.models import Profile


#class ProfileAdmin(admin.ModelAdmin):
#    pass
#    list_display = ['pk', 'url', 'title', 'parent', 'name', ]
#    list_display_links = ['pk', 'url', 'title', ]
#    fieldsets = [
#        (None,               {'classes': ['wide'], 'fields': ['parent', 'url', 'title', 'name', 'description', ], }),
#        ('Meta information', {'classes': ['collapse'], 'fields': ['meta_title', 'meta_description',
# 'meta_keywords', ], }),
#        ('Additional information', {'classes': ['collapse'], 'fields': ['template', 'visibility', ], })
#    ]
#    readonly_fields = (u'url', )
    #    prepopulated_fields = {u'url' : (u'title',), }

#    prepopulated_fields = {'url' : ('title',), }

#    inlines = [
#        PhotoInLine,
#    ]
#    save_as = True
#    save_on_top = True

#from apps.product.models import Information


#class InformationInLine(admin.TabularInline):
#    model = Information
#    extra = 5


#admin.site.register(Profile, ProfileAdmin, )
