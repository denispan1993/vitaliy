# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

__author__ = 'Alex Starov'


urlpatterns = patterns('apps.adminSite.delivery.views',
                       url(regex=ur'^панель/список/$',
                           view='index',
                           kwargs={'template_name': u'delivery/index.jinja2', },
                           name='index', ),
                       url(regex=ur'^панель/редактор/(?P<delivery_id>\d{6})/$',
                           view='add_edit',
                           kwargs={'template_name': u'delivery/add_edit.jinja2', },
                           name='edit', ),
                       url(regex=ur'^панель/редактор/рассылка/добавить/$',
                           view='add_edit',
                           kwargs={'delivery_id': None,
                                   'template_name': u'delivery/add_edit.jinja2', },
                           name='add', ),
                       url(regex=ur'^запуск/тестовая/(?P<delivery_id>\d{6})/$',
                           view='start_delivery',
                           kwargs={'delivery_type': 'test', },
                           name='start_delivery_test', ),
                       url(regex=ur'^запуск/главная/(?P<delivery_id>\d{6})/$',
                           view='start_delivery',
                           kwargs={'delivery_type': 'general', },
                           name='start_delivery_general', ),
                       url(regex=ur'^исключить/email/$',
                           view='exclude_email_from_delivery',
                           kwargs={'template_name': None, },
                           name='exclude_email_from_delivery', ),
                       )
