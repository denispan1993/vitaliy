# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from apps.yandex.views import GenerateShopYMLView

__author__ = 'AlexStarov'


urlpatterns = patterns('',
                       url(regex=r'^shop.yml$',
                           view=GenerateShopYMLView.as_view(),
                           # kwargs={'template_name': u'show_cart.jinja2', },
                           name='show_yml', ),
                       )
