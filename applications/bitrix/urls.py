# -*- coding: utf-8 -*-
from django.conf.urls import url, include

from . import dispatcher

__author__ = 'AlexStarov'


app_urlpatterns = [
    url(r'^import/$', dispatcher.front_view, name='front_view'),
    url(r'^export/$', dispatcher.front_view, name='front_view'),
]

urlpatterns = [
    url(r'^exchange/', include(app_urlpatterns, namespace='cml', app_name='cml')),
]

# from .views import ExchangeView

# urlpatterns = [url(regex=r'^exchange/$',
#                    view=ExchangeView.as_view(),
#                    name='exchange', ), ]
