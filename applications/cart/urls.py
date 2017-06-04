# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.views.generic import TemplateView

from .cart import show_cart, recalc_cart
from .order import ordering_step_one, ordering_step_two, result_ordering, order_success

__author__ = 'AlexStarov'


urlpatterns = [url(regex=r'^$',
                   view=show_cart,
                   kwargs={'template_name': u'show_cart.jinja2', },
                   name='show_cart', ),
               url(regex=r'^пересчитать/$',
                   view=recalc_cart,
                   name='recalc_cart', ), ]

urlpatterns += [url(regex=r'^первый-шаг/$',
                    view=ordering_step_one,
                    kwargs={'template_name': u'order/step_one.jinja2', },
                    name='ordering_step_one_ru', ),
                url(regex=r'^второй-шаг/$',
                    view=ordering_step_two,
                    kwargs={'template_name': u'order/step_two_ua.jinja2', },
                    name='ordering_step_two_ru', ),
                url(regex=r'^результат-оформления/$',
                    view=result_ordering,
                    kwargs=None,
                    name='result_ordering_ru', ),
                url(regex=r'^оформление-прошло-успешно/$',
                    view=order_success,
                    kwargs={'template_name': 'order/successful.jinja2', },
                    name='successful_ru', ),
                url(regex=r'^вы-где-то-оступились/$',
                    view=TemplateView.as_view(template_name='order/unsuccessful.jinja2'),
                    name='unsuccessful_ru', ),
                url(regex=r'^процесс-обработки-заказа-уже-запущен/$',
                    view=TemplateView.as_view(template_name='order/processing.jinja2'),
                    name='already_processing_ru', ), ]
