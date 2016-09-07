# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from apps.utils.decorators import manager_required, member_required
from apps.adminSite.coupon.views import CouponGroupCreateEdit, CouponCreateEdit

__author__ = 'AlexStarov'


#Admin panel
urlpatterns = patterns('apps.adminSite.coupon.views',
                       # """ Админ панель Купонов. """
                       url(regex=ur'^группа/поиск/$',
                           view='coupon_group_search',
                           kwargs={'template_name': u'coupon/group_index.jinja2', },
                           name='search', ),
                       url(regex=ur'^группа/редактор/добавить/$',
                           view=manager_required(CouponGroupCreateEdit.as_view(), ),
                           name='coupon_group_add', ),
                       url(regex=ur'^группа/редактор/(?P<coupon_group_id>\d{6})/$',
                           view=manager_required(CouponGroupCreateEdit.as_view(), ),
                           name='coupon_group_edit', ),
                       )
urlpatterns += patterns('',
                        url(regex=ur'^редактор/добавить/$',
                            view=manager_required(CouponCreateEdit.as_view(), ),
                            name='coupon_add', ),
                        url(regex=ur'^редактор/(?P<coupon_id>\d{6})/$',
                            view=manager_required(CouponCreateEdit.as_view(), ),
                            name='coupon_edit', ),
                        )
