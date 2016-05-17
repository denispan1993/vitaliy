# -*- coding: utf-8 -*-
from django.contrib import admin
from apps.mycalendar.models import LeadingCourse, CoordinatorCourse, LocationDate, Section, Topic, Event

__author__ = 'AlexStarov'


class LeadingCourseAdmin(admin.ModelAdmin, ):
    list_display = ['pk', 'surname', 'name', 'patronymic', 'created_at', 'updated_at', ]
    list_display_links = ['pk', 'surname', 'name', ]
    search_fields = ('surname', 'name', )

    prepopulated_fields = {u'url': (u'surname', u'name', u'patronymic', ), }

    class Media:
        js = ('/media/js/admin/ruslug-urlify.js', )

admin.site.register(LeadingCourse, LeadingCourseAdmin, )


class CoordinatorCourseAdmin(admin.ModelAdmin, ):
    list_display = ['pk', 'surname', 'name', 'patronymic', 'created_at', 'updated_at', ]
    list_display_links = ['pk', 'surname', 'name', ]
    search_fields = ('surname', 'name', )

    prepopulated_fields = {u'url': (u'surname', u'name', u'patronymic', ), }

    class Media:
        js = ('/media/js/admin/ruslug-urlify.js', )

admin.site.register(CoordinatorCourse, CoordinatorCourseAdmin, )
#    list_display = ['pk', 'url', 'title', 'parent', 'name', ]
#    list_display_links = ['pk', 'url', 'title', ]
#    fieldsets = [
#        (None,               {'classes': ['wide'], 'fields': ['parent', 'is_active', 'disclose_product', 'url',
#                                                              'title', 'name', 'description', ], }),
#        (u'Информация о категории для поисковых систем', {'classes': ['collapse'], 'fields': ['meta_title',
#                                                                                              'meta_description',
#                                                                                              'meta_keywords', ], }),
#        (u'Дополнительные функции', {'classes': ['collapse'], 'fields': ['template', 'visibility', ], })
#    ]
#    readonly_fields = (u'url', )
#    prepopulated_fields = {u'url' : (u'title',), }

#    prepopulated_fields = {'url' : ('title',), }

#    inlines = [
#        GenericStacked_Photo_InLine,
#    ]
#    save_as = True
#    save_on_top = True

#    class Media:
#        js = ('/media/js/admin/ruslug-urlify.js', )


class LocationDateAdmin(admin.ModelAdmin, ):
    list_display = ['pk', 'city', 'date_start', 'coordinator', 'created_at', 'updated_at', ]
    list_display_links = ['pk', 'city', 'coordinator', ]
admin.site.register(LocationDate, LocationDateAdmin, )


class SectionAdmin(admin.ModelAdmin, ):
    list_display = ['pk', 'section', 'created_at', 'updated_at', ]
    list_display_links = ['pk', 'section', ]
    search_fields = ('section', )
admin.site.register(Section, SectionAdmin, )


class TopicAdmin(admin.ModelAdmin, ):
    list_display = ['pk', 'topic', 'created_at', 'updated_at', ]
    list_display_links = ['pk', 'topic', ]
    search_fields = ('topic', )
admin.site.register(Topic, TopicAdmin, )


class EventAdmin(admin.ModelAdmin, ):
    list_display = ['pk', 'leading_course', 'section', 'topic', 'title', 'created_at', 'updated_at', ]
    list_display_links = ['pk', 'section', 'topic', ]
    search_fields = ('section', 'topic', )

    filter_horizontal = ('location_date', )

admin.site.register(Event, EventAdmin, )
