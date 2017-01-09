# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.views.generic import TemplateView

__author__ = 'AlexStarov'


urlpatterns = patterns('apps.cart.order',
                       url(regex=ur'^первый-шаг/$',
                           view='ordering_step_one',
                           kwargs={'template_name': u'order/step_one.jinja2', },
                           name='ordering_step_one_ru', ),
                       url(regex=ur'^второй-шаг/$',
                           view='ordering_step_two',
                           kwargs={'template_name': u'order/step_two_ua.jinja2', },
                           name='ordering_step_two_ru', ),
                       url(regex=ur'^результат-оформления/$',
                           view='result_ordering',
                           kwargs=None,
                           name='result_ordering_ru', ),
                       url(regex=ur'^оформление-прошло-успешно/$',
                           view='order_success',
                           kwargs={'template_name': 'order/successful.jinja2', },
                           name='successful_ru', ),
                       url(regex=ur'^вы-где-то-оступились/$',
                           view=TemplateView.as_view(template_name='order/unsuccessful.jinja2'),
                           name='unsuccessful_ru', ),
                       url(regex=ur'^процесс-обработки-заказа-уже-запущен/$',
                           view=TemplateView.as_view(template_name='order/processing.jinja2'),
                           name='already_processing_ru', ),
                       )
