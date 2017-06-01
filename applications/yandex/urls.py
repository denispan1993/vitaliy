# -*- coding: utf-8 -*-
from django.conf.urls import url

from applications.yandex.views import GenerateShopYMLView

__author__ = 'AlexStarov'


urlpatterns = [url(regex=r'^shop.yml$',
                   view=GenerateShopYMLView.as_view(),
                   name='show_yml', ), ]