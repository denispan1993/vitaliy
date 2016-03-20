# -*- coding: utf-8 -*-
__author__ = 'AlexStarov'

from django.conf.urls import patterns, url
from apps.opinion import views

urlpatterns = patterns('',
                       url(regex=r'^add/$',
                           view=views.OpinionAddView.as_view(),
                           name='add_en', ),
                       url(regex=ur'^добавить/$',
                           view=views.OpinionAddView.as_view(),
                           name='add_ru', ),

                       url(regex=r'^adding/$',
                           view=views.OpinionAddingView.as_view(),
                           name='adding_en', ),
                       url(regex=ur'^добавление/$',
                           view=views.OpinionAddingView.as_view(),
                           name='adding_ru', ),

                       url(regex=r'^successfuly/added/$',
                           view=views.OpinionAddedView.as_view(),
                           name='added_successfully_en',
                           kwargs={'succesfully': True}),
                       url(regex=ur'^успешно/добавлен/$',
                           view=views.OpinionAddedView.as_view(),
                           name='added_successfully_ru',
                           kwargs={'succesfully': True}),

                       url(regex=r'^not-added/$',
                           view=views.OpinionAddedView.as_view(),
                           name='added_not-successfully_en',
                           kwargs={'succesfully': False}),
                       url(regex=ur'^не-добавлен/$',
                           view=views.OpinionAddedView.as_view(),
                           name='added_not-successfully_ru',
                           kwargs={'succesfully': False}),

                       url(regex=r'^list/$',
                           view=views.OpinionListView.as_view(),
                           name='list_en', ),
                       url(regex=ur'^список/$',
                           view=views.OpinionListView.as_view(),
                           name='list_ru', ),

                       url(regex=ur'^(?P<opinion_url>[а-яА-Яa-zA-ZёЁїЇіІґҐєЄ0-9_.-]+)/(?P<pk>\d{6})/$',
                           view=views.OpinionDetailView.as_view(),
                           name='opinion_long', ),
                       url(regex=ur'^(?P<pk>\d{6})/$',
                           view=views.OpinionDetailView.as_view(),
                           name='opinion_short', ),
                       )
