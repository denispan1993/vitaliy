# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from apps.utils.decorators import manager_required
from .coupon.views import CouponGroupCreateEdit, CouponCreateEdit
from .sms_ussd.views import SendSMSCreateView

__author__ = 'AlexStarov'

#Admin panel
urlpatterns = patterns('apps.adminSite',
                       url(regex=ur'^$',
                           view='views.admin_panel',
                           kwargs={'template_name': u'admin_panel.jinja2', },
                           name='index', ),
                       )

# """ Админ панель Комментариев. """
urlpatterns += patterns('apps.adminSite.views',
                        url(ur'^комментарий/поиск/$', 'comment_search',
                            {'template_name': u'comment/comment_search.jinja2', },
                            name='comment_search', ),
                        url(ur'^комментарий/редактор/(?P<id>\d{6})/$', 'comment_edit',
                            {'template_name': u'comment/comment_edit.jinja2', },
                            name='comment_edit', ),
                        )

# """ Админ панель Заказов. """
urlpatterns += patterns('apps.adminSite.order.views',
                        url(regex=ur'^заказ/поиск/$',
                            view='order_search',
                            kwargs={'template_name': u'order/order_search.jinja2', },
                            name='order_search', ),
                        url(regex=ur'^заказ/редактор/(?P<order_id>\d{6})/$',
                            view='order_edit',
                            kwargs={'template_name': u'order/order_edit.jinja2', },
                            name='order_edit', ),
                        url(regex=ur'^заказ/редактор/товар/добавить/(?P<order_id>\d{6})/$',
                            view='order_edit_product_add',
                            kwargs={'template_name': u'order/order_edit_product_add.jinja2', },
                            name='order_edit_product_add', ),
                        )

# """ Админ панель Купонов. """
urlpatterns += patterns('apps.adminSite.coupon.views',
                        # """ Админ панель Купонов. """
                        url(regex=ur'^купон/группа/поиск/$',
                            view='coupon_group_search',
                            kwargs={'template_name': u'coupon/group_index.jinja2', },
                            name='search', ),
                        url(regex=ur'^купон/группа/редактор/добавить/$',
                            view=manager_required(CouponGroupCreateEdit.as_view(), ),
                            name='coupon_group_add', ),
                        url(regex=ur'^купон/группа/редактор/(?P<coupon_group_id>\d{6})/$',
                            view=manager_required(CouponGroupCreateEdit.as_view(), ),
                            name='coupon_group_edit', ),
                        )
urlpatterns += patterns('',
                        url(regex=ur'^купон/редактор/добавить/$',
                            view=manager_required(CouponCreateEdit.as_view(), ),
                            name='coupon_add', ),
                        url(regex=ur'^купон/редактор/(?P<coupon_id>\d{6})/$',
                            view=manager_required(CouponCreateEdit.as_view(), ),
                            name='coupon_edit', ),
                        )


# """ Админ панель Рассылок. """
urlpatterns += patterns('apps.adminSite.delivery.views',
                        url(regex=ur'^рассылка/панель/список/$',
                            view='index',
                            kwargs={'template_name': u'delivery/index.jinja2', },
                            name='delivery_index', ),
                        url(regex=ur'^рассылка/панель/редактор/(?P<delivery_id>\d{6})/$',
                            view='add_edit',
                            kwargs={'template_name': u'delivery/add_edit.jinja2', },
                            name='edit', ),
                        url(regex=ur'^рассылка/панель/редактор/рассылка/добавить/$',
                            view='add_edit',
                            kwargs={'delivery_id': None,
                                    'template_name': u'delivery/add_edit.jinja2', },
                            name='add', ),
                        url(regex=ur'^рассылка/запуск/тестовая/(?P<delivery_id>\d{6})/$',
                            view='start_delivery',
                            kwargs={'delivery_type': 'test', },
                            name='start_delivery_test', ),
                        url(regex=ur'^рассылка/запуск/главная/(?P<delivery_id>\d{6})/$',
                            view='start_delivery',
                            kwargs={'delivery_type': 'general', },
                            name='start_delivery_general', ),
                        url(regex=ur'^рассылка/исключить/email/$',
                            view='exclude_email_from_delivery',
                            kwargs={'template_name': None, },
                            name='exclude_email_from_delivery', ),
                        )

# """ Админ панель SMS USSD. """
urlpatterns += patterns('',
                        url(regex=ur'^sms_ussd/send_sms/$',
                            view=SendSMSCreateView.as_view(),
                            name='sms_ussd_send_sms', ),
                        )
