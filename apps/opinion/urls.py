# -*- coding: utf-8 -*-
__author__ = 'AlexStarov'

from django.conf.urls import patterns, url
from apps.opinion import views

urlpatterns = patterns('',
                       url(regex=r'^list/$',
                           view=views.OpinionListView.as_view(),
                           name='list_en', ),
                       url(regex=ur'^список/$',
                           view=views.OpinionListView.as_view(),
                           name='list_ru', ),
                       url(regex=r'^add/$',
                           view=views.OpinionListView.as_view(),
                           name='add_en', ),
                       url(regex=ur'^добавить/$',
                           view=views.OpinionListView.as_view(),
                           name='add_ru', ),
                       url(regex=ur'^(?P<opinion_url>[а-яА-Яa-zA-ZёЁїЇіІґҐєЄ0-9_.-]+)/(?P<pk>\d{6})/$',
                           view=views.OpinionDetailView.as_view(),
                           name='opinion_long', ),
                       url(regex=ur'^(?P<pk>\d{6})/$',
                           view=views.OpinionDetailView.as_view(),
                           name='opinion_short', ),
                       )
