# coding=utf-8
__author__ = 'user'

try:
    from django.conf.urls import patterns, include, url
    from django.conf.urls.i18n import i18n_patterns
except ImportError:  # django < 1.4
    from django.conf.urls.defaults import patterns, include, url


from apps.utils.decorators import manager_required, member_required
from apps.adminSite.coupon.views import CouponGroupCreateEdit, CouponCreateEdit
#Admin panel
urlpatterns = patterns('apps.adminSite.coupon.views',
                       # """ Админ панель Купонов. """
                       url(ur'^группа/поиск/$', 'coupon_group_search',
                           {'template_name': u'coupon/coupon_group_search.jinja2.html', },
                           name='coupon_group_search', ),
                       url(ur'^группа/редактор/добавить/$',
                           manager_required(CouponGroupCreateEdit.as_view(), ),
                           name='coupon_group_add', ),
                       url(ur'^группа/редактор/(?P<coupon_group_id>\d{6})/$',
                           manager_required(CouponGroupCreateEdit.as_view(), ),
                           name='coupon_group_edit', ),
                       )
urlpatterns += patterns('',
                        url(ur'^редактор/добавить/$',
                            manager_required(CouponCreateEdit.as_view(), ),
                            name='coupon_add', ),
                        url(ur'^редактор/(?P<coupon_id>\d{6})/$',
                            manager_required(CouponCreateEdit.as_view(), ),
                            name='coupon_edit', ),
                        )
