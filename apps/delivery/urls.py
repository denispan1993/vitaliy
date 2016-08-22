# -*- coding: utf-8 -*-
from django.conf.urls import url
from apps.delivery import views

__author__ = 'AlexStarov'


urlpatterns = [
    url(regex=r'^$',
        view=views.ClickView.as_view(),
        name='click', ),
    url(r'^(?P<mid>[A-f0-9-]+).gif$',
        views.OpenView.as_view(), name='open'),
    url(r'^(?P<mid>[A-f0-9-]+)/(?P<hash>[A-f0-9]+)/$',
        views.ClickView.as_view(), name='click'),
]
