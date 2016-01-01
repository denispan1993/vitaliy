# -*- coding: utf-8 -*-
__author__ = 'AlexStarov'

from django.conf.urls import patterns, url, include


urlpatterns = patterns('apps.payment',
                       url(regex=ur'^(?P<id>\d{6})/$',
                           view='views.root',
                           kwargs={'template_name': u'payment.jinja2', },
                           name='ordering_step_one_ru', ),
#                       url(regex=ur'^paypal/$',
#                           view='ordering_step_one',
#                           # kwargs=None,
#                           kwargs={'template_name': u'order/step_one.jinja2', },
#                           name='ordering_step_one_ru', ),
                       url(regex=r'^paypal/ipn/',
                           view=include('paypal.standard.ipn.urls'), ),
                       )
