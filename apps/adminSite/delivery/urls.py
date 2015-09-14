# -*- coding: utf-8 -*-
__author__ = 'Alex Starov'

from django.conf.urls import patterns, include, url


urlpatterns = patterns('apps.adminSite.delivery.views',
                       url(regex=ur'^панель/список/$',
                           view='index',
                           kwargs={'template_name': u'delivery/index.jingo.html', },
                           name='index', ),
                       #url(regex=ur'^панель/редактор/(?P<delivery_id>\d{6})/$',
                       url(regex=ur'^панель/редактор/(?P<delivery_id>\d)/$',
                           view='add_edit',
                           kwargs={'template_name': u'delivery/add_edit.jingo.html', },
                           name='edit', ),
                       url(regex=ur'^панель/редактор/рассылка/добавить/$',
                           view='add_edit',
                           kwargs={'delivery_id': None,
                                   'template_name': u'delivery/add_edit.jingo.html', },
                           name='add', ),
                       )
