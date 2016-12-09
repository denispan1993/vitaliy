# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from .views import  Exchange

__author__ = 'AlexStarov'


urlpatterns = patterns('apps.bitrix.views',
                       url(regex=r'^exchange/$',
                           view=Exchange.as_view(),
                           name='exchange', ),
                       )
