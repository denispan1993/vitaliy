# -*- coding: utf-8 -*-
__author__ = 'Alex Starov'

from django.conf.urls import patterns, include, url


urlpatterns = patterns('apps.adminSite.delivery.views',
                       url(regex=ur'^панель/список/$',
                           view='index',
                           kwargs={'template_name': u'delivery/index.jinja2.html', },
                           name='index', ),
                       url(regex=ur'^панель/редактор/(?P<delivery_id>\d{6})/$',
                           view='add_edit',
                           kwargs={'template_name': u'delivery/add_edit.jingo.html', },
                           name='edit', ),
                       url(regex=ur'^панель/редактор/рассылка/добавить/$',
                           view='add_edit',
                           kwargs={'delivery_id': None,
                                   'template_name': u'delivery/add_edit.jingo.html', },
                           name='add', ),
                       url(regex=ur'^запуск/тестовая/(?P<delivery_id>\d{6})/$',
                           view='start_delivery',
                           kwargs={'delivery_type': 'test', 'template_name': None, },
                           name='start_delivery_test', ),
                       url(regex=ur'^запуск/главная/(?P<delivery_id>\d{6})/$',
                           view='start_delivery',
                           kwargs={'delivery_type': 'general', 'template_name': None, },
                           name='start_delivery_general', ),
                       )
