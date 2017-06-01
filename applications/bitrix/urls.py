# -*- coding: utf-8 -*-
from django.conf.urls import url

from .views import ExchangeView

__author__ = 'AlexStarov'


urlpatterns = [url(regex=r'^exchange/$',
                   view=ExchangeView.as_view(),
                   name='exchange', ), ]
