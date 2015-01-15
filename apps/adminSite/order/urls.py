# coding=utf-8
__author__ = 'user'

try:
    from django.conf.urls import patterns, include, url
    from django.conf.urls.i18n import i18n_patterns
except ImportError:  # django < 1.4
    from django.conf.urls.defaults import patterns, include, url


#from apps.utils.decorators import manager_required, member_required
#from apps.adminSite.coupon import CouponGroupCreateEdit, CouponCreateEdit

urlpatterns = patterns('apps.adminSite.order.views',
                       url(ur'^поиск/$', 'order_search',
                           {'template_name': u'order/order_search.jinja2.html', },
                           name='order_search', ),
                       url(ur'^редактор/(?P<id>\d{6})/$', 'order_edit',
                           {'template_name': u'order/order_edit.jinja2.html', },
                           name='order_edit', ),
                       url(ur'^редактор/товар/добавить/(?P<order_id>\d{6})/$', 'order_edit_product_add',
                           {'template_name': u'order/order_edit_product_add.jinja2.html', },
                           name='order_edit_product_add', ),
                       )
