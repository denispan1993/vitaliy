# -*- coding: utf-8 -*-
from django.conf.urls import url

from applications.utils.captcha.views import captcha_image_show


#Captcha MAIN
urlpatterns = [url(r'(?P<filename>[a-zA-Z0-9]{8}).jpg$',
                   captcha_image_show,
                   name='captcha_image_show', ),
               ]
