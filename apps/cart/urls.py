# -*- coding: utf-8 -*-
__author__ = 'user'

from django.conf.urls import patterns, include, url
# from django.conf.urls.i18n import i18n_patterns


urlpatterns = patterns('apps.cart.order',
                       url(regex=ur'^первый-шаг/$',
                           view='ordering_step_one',
                           kwargs={'template_name': u'order/step_one.jinja2.html', },
                           name='ordering_step_one_ru', ),
                       url(regex=ur'^второй-шаг/$',
                           view='ordering_step_two',
                           kwargs={'template_name': u'order/step_two_ua.jinja2.html', },
                           name='ordering_step_two_ru', ),
                       url(regex=ur'^результат-оформления/$',
                           view='result_ordering',
                           kwargs=None,
                           name='result_ordering_ru', ),
                       url(regex=ur'^оформление-прошло-успешно/$',
                           view='order_success',
                           kwargs={'template_name': u'order/success.jinja2.html', },
                           name='order_success_ru', ),
                       url(regex=ur'^вы-где-то-оступились/$',
                           view='order_unsuccessful',
                           kwargs={'template_name': u'order/unsuccessful.jinja2.html', },
                           name='order_unsuccessful_ru', ),
                       )