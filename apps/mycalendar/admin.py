# -*- coding: utf-8 -*-
from django.contrib import admin
from apps.mycalendar.models import LeadingCourse, LocationDateTime, Subject, Event

__author__ = 'AlexStarov'


class LeadingCourseAdmin(admin.ModelAdmin, ):
    list_display = ['pk', 'surname', 'name', 'patronymic', 'created_at', 'updated_at', ]
    list_display_links = ['pk', 'surname', 'name', ]
    search_fields = ('surname', 'name', )

    prepopulated_fields = {u'url': (u'surname', u'name', u'patronymic', ), }

    class Media:
        js = ('/media/js/admin/ruslug-urlify.js', )

admin.site.register(LeadingCourse, LeadingCourseAdmin, )
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


class LocationDateTimeAdmin(admin.ModelAdmin, ):
    list_display = ['pk', 'city', 'date_start', 'date_end', 'created_at', 'updated_at', ]
    list_display_links = ['pk', 'city', ]
admin.site.register(LocationDateTime, LocationDateTimeAdmin, )


class SubjectAdmin(admin.ModelAdmin, ):
    list_display = ['pk', 'subject', 'created_at', 'updated_at', ]
    list_display_links = ['pk', 'subject', ]
    search_fields = ('subject', )
admin.site.register(Subject, SubjectAdmin, )


class EventAdmin(admin.ModelAdmin, ):
    list_display = ['pk', 'leading_course', 'subject', 'title', 'created_at', 'updated_at', ]
    list_display_links = ['pk', 'subject', ]
    search_fields = ('subject', )

    filter_horizontal = ('location_date_time', )

admin.site.register(Event, EventAdmin, )
