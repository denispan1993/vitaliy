# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from .views import AllViews

__author__ = 'AlexStarov'


urlpatterns = patterns('',
                       url(regex=ur'^$',
                           view=AllViews.as_view(),
                           name='all_ru', ),
                       )

urlpatterns += patterns('apps.mycalendar.views',
                       url(regex=ur'^ведущий/(?P<leading_course_url>[а-яА-Яa-zA-ZёЁїЇіІґҐєЄ0-9_.-]+)/$',
                           view='leading_course',
                           kwargs={'template_name': u'leading_course.jinja2', },
                           name='leading_course_ru', ),
                       url(regex=ur'^годы/$',
                           view='years',
                           kwargs={'template_name': u'years.jinja2', },
                           name='years_ru', ),
                       url(regex=ur'^(?P<year>\d{4})/$',
                           view='year',
                           kwargs={'template_name': u'year.jinja2', },
                           name='year', ),
                       url(regex=ur'(?P<year>\d{4})/(?P<month>\d{2})/$',
                           view='month',
                           kwargs={'template_name': u'month.jinja2', },
                           name='month', ),
                       )
