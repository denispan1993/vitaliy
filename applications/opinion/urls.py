# -*- coding: utf-8 -*-

from django.conf.urls import url
from applications.opinion import views

__author__ = 'AlexStarov'

urlpatterns = [url(regex=r'^add/$', view=views.OpinionAddView.as_view(), name='add_en', ),\
               url(regex=ur'^добавить/$', view=views.OpinionAddView.as_view(), name='add_ru', ),
               url(regex=r'^successfuly/added/$', view=views.OpinionAddedView.as_view(),
                   name='added_successfully_en', kwargs={'successfully': True}, ),
               url(regex=ur'^успешно/добавлен/$', view=views.OpinionAddedView.as_view(),
                   name='added_successfully_ru', kwargs={'successfully': True}, ),
               url(regex=r'^not-added/$', view=views.OpinionAddedView.as_view(),
                   name='added_not-successfully_en', kwargs={'successfully': False}, ),
               url(regex=ur'^не-добавлен/$', view=views.OpinionAddedView.as_view(),
                   name='added_not-successfully_ru', kwargs={'successfully': False}),
               url(regex=r'^$', view=views.OpinionListView.as_view(), name='list', ),
               url(regex=ur'^(?P<opinion_url>[а-яА-Яa-zA-ZёЁїЇіІґҐєЄ0-9_.-]+)/(?P<pk>\d+)/$',
                   view=views.OpinionDetailView.as_view(),
                   name='opinion_long', ),
               url(regex=ur'^(?P<pk>\d+)/$',
                   view=views.OpinionDetailView.as_view(),
                   name='opinion_short', ), ]
