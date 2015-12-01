# -*- coding: utf-8 -*-
__author__ = 'AlexStarov'

from django.conf.urls import patterns, url


urlpatterns = patterns('apps.calendar.views',
                       url(regex=ur'^все/$',
                           view='all',
                           kwargs={'template_name': u'all.jinja2', },
                           name='all1_ru', ),
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
