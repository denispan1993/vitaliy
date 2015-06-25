# -*- coding: utf-8 -*-
__author__ = 'Alex Starov'
try:
    from django.conf.urls import patterns, include, url
    from django.conf.urls.i18n import i18n_patterns
except ImportError:  # django < 1.4
    from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('apps.ajax.coupon',
                       url(r'^test/$', 'coupon_test',
                           name='ajax_coupon_text', ),
                       )
urlpatterns += patterns('apps.ajax.slides',
                        url(r'^left/$', 'left',
                            name='ajax_slide_left', ),
                        )
#/ajax/order/
urlpatterns += patterns('apps.ajax.views',
                        url(r'^change/$', 'order_change',
                            name='ajax_order_change', ),
                        url(r'^add/search/$', 'order_add_search',
                            name='ajax_order_add_search', ),
                        url(r'^add/$', 'order_add',
                            name='ajax_order_add', ),
                        )
urlpatterns += patterns('apps.ajax.order',
                        url(r'^email/test/$', 'order_email_test',
                            name='ajax_order_email_test', ),
                        )

urlpatterns += patterns('apps.ajax.callback',
                        url(r'^send/$', 'callback_data_send',
                            name='ajax_callback_data_send', ),
                        )
urlpatterns += patterns('apps.ajax.feedback',
                        url(r'^send/$', 'feedback_data_send',
                            name='ajax_feedback_data_send', ),
                        )
