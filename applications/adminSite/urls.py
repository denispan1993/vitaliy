# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import url
from applications.utils.decorators import manager_required

from .sms_ussd.views import SMS_USSDPanelView, SendSMSCreateView, SendUSSDCreateView

from .views import admin_panel, comment_search, comment_edit
from .order.views import order_search, order_edit, order_edit_product_add
from .coupon.views import coupon_group_search, CouponGroupCreateEdit, CouponCreateEdit
from .delivery.views import index, add_edit, start_delivery, exclude_email_from_delivery

__author__ = 'AlexStarov'


""" Admin panel """
urlpatterns = [url(regex=r'^$',
                   view=admin_panel,
                   kwargs={'template_name': u'admin_panel.html', },
                   name='index', ), ]

""" Админ панель Комментариев. """
urlpatterns += [url(regex=r'^комментарий/поиск/$',
                    view=comment_search,
                    kwargs={'template_name': u'comment/comment_search.jinja2', },
                    name='comment_search', ),
                url(regex=r'^комментарий/редактор/(?P<id>\d{6})/$',
                    view=comment_edit,
                    kwargs={'template_name': u'comment/comment_edit.jinja2', },
                    name='comment_edit', ), ]

""" Админ панель Заказов. """
urlpatterns += [url(regex=r'^заказ/поиск/$',
                    view=order_search,
                    kwargs={'template_name': u'order/order_search.jinja2', },
                    name='order_search', ),
                url(regex=r'^заказ/редактор/(?P<order_id>\d{6})/$',
                    view=order_edit,
                    kwargs={'template_name': u'order/order_edit.jinja2', },
                    name='order_edit', ),
                url(regex=r'^заказ/редактор/товар/добавить/(?P<order_id>\d{6})/$',
                    view=order_edit_product_add,
                    kwargs={'template_name': u'order/order_edit_product_add.jinja2', },
                    name='order_edit_product_add', ), ]

""" Админ панель Купонов. """
urlpatterns += [url(regex=r'^купон/группа/поиск/$',
                    view=coupon_group_search,
                    kwargs={'template_name': u'coupon/group_index.jinja2', },
                    name='coupon_group_index', ),
                url(regex=r'^купон/группа/редактор/добавить/$',
                    view=manager_required(CouponGroupCreateEdit.as_view(), ),
                    name='coupon_group_add', ),
                url(regex=r'^купон/группа/редактор/(?P<coupon_group_id>\d{6})/$',
                    view=manager_required(CouponGroupCreateEdit.as_view(), ),
                    name='coupon_group_edit', ),
                url(regex=r'^купон/редактор/добавить/$',
                    view=manager_required(CouponCreateEdit.as_view(), ),
                    name='coupon_add', ),
                url(regex=r'^купон/редактор/(?P<coupon_id>\d{6})/$',
                    view=manager_required(CouponCreateEdit.as_view(), ),
                    name='coupon_edit', ), ]

""" Админ панель Рассылок. """
urlpatterns += [url(regex=r'^рассылка/панель/список/$',
                    view=index,
                    kwargs={'template_name': u'delivery/index.jinja2', },
                    name='delivery_index', ),
                url(regex=r'^рассылка/панель/редактор/(?P<delivery_id>\d{6})/$',
                    view=add_edit,
                    kwargs={'template_name': u'delivery/add_edit.jinja2', },
                    name='edit', ),
                url(regex=r'^рассылка/панель/редактор/рассылка/добавить/$',
                    view=add_edit,
                    kwargs={'delivery_id': None,
                            'template_name': u'delivery/add_edit.jinja2', },
                    name='add', ),
                url(regex=r'^рассылка/запуск/тестовая/(?P<delivery_id>\d{6})/$',
                    view=start_delivery,
                    kwargs={'delivery_type': 'test', },
                    name='start_delivery_test', ),
                url(regex=r'^рассылка/запуск/главная/(?P<delivery_id>\d{6})/$',
                    view=start_delivery,
                    kwargs={'delivery_type': 'general', },
                    name='start_delivery_general', ),
                url(regex=r'^рассылка/исключить/email/$',
                    view=exclude_email_from_delivery,
                    kwargs={'template_name': None, },
                    name='exclude_email_from_delivery', ), ]

""" Админ панель SMS USSD. """
urlpatterns += [url(regex=r'^sms_ussd/$',
                    view=SMS_USSDPanelView.as_view(),
                    name='sms_ussd_panel', ), ]
urlpatterns += [url(regex=r'^sms_ussd/send_sms/$',
                    view=SendSMSCreateView.as_view(),
                    name='sms_ussd_send_sms', ), ]
urlpatterns += [url(regex=r'^sms_ussd/send_ussd/$',
                    view=SendUSSDCreateView.as_view(),
                    name='sms_ussd_send_ussd', ), ]
