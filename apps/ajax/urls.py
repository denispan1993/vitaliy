# coding=utf-8
try:
    from django.conf.urls import patterns, include, url
    from django.conf.urls.i18n import i18n_patterns
except ImportError:  # django < 1.4
    from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('apps.ajax.coupon',
                       url(r'^test/$', 'coupon_test',
                           name='ajax_coupon_text', ),
                       )
