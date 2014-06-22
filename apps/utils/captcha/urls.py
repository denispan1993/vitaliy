# coding=utf-8
try:
    from django.conf.urls import patterns, include, url
except ImportError:  # django < 1.4
    from django.conf.urls.defaults import patterns, include, url

#Captcha MAIN
urlpatterns = patterns('apps.utils.captcha.views',
                       url(r'(?P<filename>[a-zA-Z0-9]{8}).jpg$',
                           'captcha_image_show',
                           # {'template_name': u'category/show_basement_category.jinja2.html', },
                           name='captcha_image_show', ),
                       )
