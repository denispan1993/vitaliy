# coding=utf-8
try:
    from django.conf.urls import patterns, include, url
    from django.conf.urls.i18n import i18n_patterns
except ImportError:  # django < 1.4
    from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('apps.ajax',
                       url(r'^test/$', 'coupon.coupon_test',
                           name='ajax_coupon_text', ),
                       url(r'^left/$', 'slides.left',
                           name='ajax_slide_left', ),
                       )
