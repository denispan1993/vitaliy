# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from .views import  ExchangeView

__author__ = 'AlexStarov'


urlpatterns = patterns('apps.bitrix.views',
                       url(regex=r'^exchange/$',
                           view=ExchangeView.as_view(),
                           name='exchange', ),
                       )
