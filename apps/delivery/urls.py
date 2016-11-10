# -*- coding: utf-8 -*-
from django.conf.urls import url
from apps.delivery import views

__author__ = 'AlexStarov'


urlpatterns = [
# aaa=re.compile(r'^\?(?P<key>[a-zA-Z0-9]{64,64})$')
# print re.match(aaa, '?naJX2WhVXlGtXlg0NFhbY1hqXu51M8MyUzwxpLm1SBvdcWerdNDRJPmtXmZYR0qe').group('key')
#    url(regex=r'^\?(?P<key>[a-zA-Z0-9]{64,64})$', --> это правильное выражение
    url(regex=r'^$',
        view=views.ClickView.as_view(),
        name='click', ),
    url(regex=r'^track/(?P<key>[a-zA-Z0-9]{64})/opened/$',
        view=views.OpenView.as_view(),
        name='open', ),
#    url(r'^(?P<mid>[A-f0-9-]+)/(?P<hash>[A-f0-9]+)/$',
#        views.ClickView.as_view(), name='click'),
]
