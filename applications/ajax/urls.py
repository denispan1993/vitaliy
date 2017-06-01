# -*- coding: utf-8 -*-
from django.conf.urls import url

from .coupon import coupon_test
from .slides import left
from .views import order_change, order_add_search, order_add
from .order import order_email_test
from .callback import callback_data_send
from .feedback import feedback_data_send
from timezone import client_timezone
from .geoip import resolve_client_geolocation

__author__ = 'AlexStarov'

urlpatterns = [url(regex=r'^test/$', view=coupon_test, name='ajax_coupon_text', ), ]

urlpatterns += [url(regex=r'^left/$', view=left, name='ajax_slide_left', ), ]

#/ajax/order/
urlpatterns += [url(regex=r'^change/$', view=order_change, name='ajax_order_change', ),
                url(regex=r'^add/search/$', view=order_add_search, name='ajax_order_add_search', ),
                url(regex=r'^add/$', view=order_add, name='ajax_order_add', ), ]
urlpatterns += [url(regex=r'^email/test/$', view=order_email_test, name='ajax_order_email_test', ), ]

urlpatterns += [url(regex=r'^call/send/$', view=callback_data_send, name='ajax_callback_data_send', ), ]
urlpatterns += [url(regex=r'^feed/send/$', view=feedback_data_send, name='ajax_feedback_data_send', ), ]
urlpatterns += [url(regex=r'^client/$', view=client_timezone, name='ajax_timezone_data_send', ), ]
urlpatterns += [url(regex=r'^resolve/$', view=resolve_client_geolocation, name='ajax_geolocation_resolve', ), ]
