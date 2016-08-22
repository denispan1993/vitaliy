# -*- coding: utf-8 -*-
# from django.conf.urls import patterns, include, url
try:
    from django.conf.urls import patterns, include, url
    # from django.conf.urls.i18n import i18n_patterns
except ImportError:  # django < 1.4
    from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

# from filebrowser.sites import site
#Admin
urlpatterns = patterns(
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls', ), ),
#    url(r'^admin/filebrowser/', include(site.urls, ), ),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls, ), ),
    url(r'^captcha/', include('apps.utils.captcha.urls', ), ),
    url(r'^redirect/', include('apps.delivery.urls', ), ),
)

#from apps.root.views import root_page
#from apps.product.views import show_category, show_product
#from apps.cart.views import show_cart
#from apps.ajax.views import resolution, cookie

urlpatterns += patterns('apps',
                        # Examples:
    # url(r'^$', 'proj.views.home', name='home'),
    url(r'^$', 'root.views.root_page',
        {'template_name': u'index.jinja2', },
        name='root_page', ),
    # url(r'^proj/', include('proj.foo.urls')),
    url(ur'^категории/$', 'product.views.show_basement_category',
        {'template_name': u'category/show_basement_category.jinja2', },
        name='show_basement_category', ),
    url(ur'^(?P<category_url>[а-яА-Яa-zA-ZёЁїЇіІґҐєЄ0-9_.-]+)/[кc](?P<id>\d{6})/$', 'product.views.show_category',
        {'template_name': u'category/show_category.jinja2', },
        name='show_category', ),
    url(ur'^(?P<product_url>[а-яА-Яa-zA-ZёЁїЇіІґҐєЄ0-9_.-]+)/[пp](?P<id>\d{6})/$', 'product.views.show_product',
        {'template_name': u'product/show_product.jinja2', },
        name='show_product', ),
    )
"""
    Раздел:
        Комментариев.
"""
urlpatterns += patterns('apps.comment',
                        url(ur'^(?P<product_url>[а-яА-Яa-zA-ZёЁїЇіІґҐєЄ0-9_.-]+)/[пp](?P<id>\d{6})/комментарий/добавить/$',
                            'views.comment_add',
                            {'template_name': u'show_comment_add.jinja2',
                             'comment_id': None, },
                            name='show_comment_add', ),
                        url(ur'^(?P<product_url>[а-яА-Яa-zA-ZёЁїЇіІґҐєЄ0-9_.-]+)/[пp](?P<id>\d{6})/комментарий/(?P<comment_id>\d{6})/добавить/$',
                            'views.comment_add',
                            {'template_name': u'show_comment_add.jinja2', },
                            name='show_comment_add', ),
                        url(ur'^(?P<product_url>[а-яА-Яa-zA-ZёЁїЇіІґҐєЄ0-9_.-]+)/[пp](?P<id>\d{6})/комментарий/добавлен/успешно/$',
                            'views.comment_add_successfully',
                            {'template_name': u'show_comment_add_successfully.jinja2', },
                            name='comment_add_successfully', ),
                        )
"""
    Раздел:
        Корзины.
"""
urlpatterns += patterns('apps.cart.views',
                        url(ur'^корзина/$', 'show_cart',
                            {'template_name': u'show_cart.jinja2', },
                            name='show_cart', ),
                        url(ur'^корзина/пересчитать/$', 'recalc_cart',
                            name='recalc_cart', ),
                        url(ur'^корзина/заказ/$', 'show_order',
                            {'template_name': u'show_order.jinja2', },
                            name='show_order', ),
                        )
urlpatterns += patterns('',
                        url(regex=ur'^заказ/',
                            view=include(arg='apps.cart.urls',
                                         namespace='cart', ),
                            ),
                        )
urlpatterns += patterns('apps.cart.views',
                        url(ur'^корзина/заказ/принят/$', 'show_order_success',
                            {'template_name': u'show_order_success.jinja2', },
                            name='show_order_success', ),
                        url(ur'^корзина/заказ/непринят/$', 'show_order_unsuccess',
                            {'template_name': u'show_order_unsuccess.jinja2', },
                            name='show_order_unsuccess', ),
                        url(ur'^корзина/order/$', 'show_order',
                            {'template_name': u'show_order.jinja2', },
                            name='show_order', ),
                        url(r'^cart/$', 'show_cart',
                            {'template_name': u'show_cart.jinja2', },
                            name='show_cart', ),
                        url(ur'^cart/заказ/$', 'show_order',
                            {'template_name': u'show_order.jinja2', },
                            name='show_order', ),
                        url(r'^cart/order/$', 'show_order',
                            {'template_name': u'show_order.jinja2', },
                            name='show_order', ),
                        )
urlpatterns += patterns('apps.currency.views',
                        url(r'^Currency/Change/$', 'currency_change',
                            name='currency_change', ),
                        url(ur'^Валюта/Изменение/$', 'currency_change',
                            name='currency_change', ),
                        )

urlpatterns += patterns('',
                        url(regex=ur'^заказ/',
                            view=include(arg='apps.cart.urls',
                                         namespace='cart', ),
                            ),
                        )

urlpatterns += patterns('',
                        url(regex=ur'^оплата/',
                            view=include(arg='apps.payment.urls',
                                         namespace='payment', ),
                            ),
                        )

#Капча
#urlpatterns += patterns(url(r'^captcha/', include('apps.utils.captcha.urls', ), ), )

#Admin panel
urlpatterns += patterns('apps.adminSite.views',
                        url(ur'^админ/$', 'admin_panel',
                            {'template_name': u'admin_panel.jinja2', },
                            name='admin_panel', ),
                        # """ Админ панель Комментариев. """
                        url(ur'^админ/комментарий/поиск/$', 'comment_search',
                            {'template_name': u'comment/comment_search.jinja2', },
                            name='comment_search', ),
                        url(ur'^админ/комментарий/редактор/(?P<id>\d{6})/$', 'comment_edit',
                            {'template_name': u'comment/comment_edit.jinja2', },
                            name='comment_edit', ),
                        )

#Search
urlpatterns += patterns('apps.search.views',
                        url(ur'^поиск/$', 'search_page',
                            {'query': None,
                             'template_name': u'category/show_category.jinja2', },
                            name='show_search', ),
                        url(ur'^поиск/(?P<query>\d+)$', 'search_page',
                            {'template_name': u'category/show_category.jinja2', },
                            name='show_search', ),
                        url(r'^search/$', 'search_page',
                            {'query': None,
                            'template_name': u'category/show_category.jinja2', },
                            name='show_search', ),
                        url(r'^search/(?P<query>\d+)$', 'search_page',
                            {'template_name': u'category/show_category.jinja2', },
                            name='show_search', ),
                        )
#Календарь
urlpatterns += patterns('',
                        url(regex=ur'^календарь/',
                            view=include(arg='apps.mycalendar.urls',
                                         namespace='calendar', ),
                            ),
                        )
urlpatterns += patterns('',
                        # """ Админ панель Заказов. """
                        url(ur'^админ/заказ/', include('apps.adminSite.order.urls'), ),
                        )

urlpatterns += patterns('',
                        # """ Админ панель Купонов. """
                        url(regex=ur'^админ/купон/',
                            view=include(arg='apps.adminSite.coupon.urls',
                                         namespace='admin_coupon', ),
                            ),
                        # """ Админ панель Рассылок. """
                        # url(regex=ur'^админ/рассылка/',
                        url(regex=ur'^админ/рассылка/',
                            view=include(arg='apps.adminSite.delivery.urls',
                                         namespace='admin_delivery', ),
                            ),
                        )
#Ajax
urlpatterns += patterns('apps.ajax.views',
                        url(r'^ajax/resolution/$', 'resolution',
                            name='ajax_resolution', ),
                        url(r'^ajax/cookie/$', 'cookie',
                            name='ajax_cookie', ),
                        url(r'^ajax/country/$', 'sel_country',
                            name='ajax_country', ),
                        url(r'^ajax/product_to_cart/$', 'product_to_cart',
                            name='ajax_product_to_cart', ),
                        )
# """ Изменение комментария """
urlpatterns += patterns('apps.ajax.comment',
                        url(r'^ajax/comment/change/$', 'comment_change',
                            name='ajax_comment_change', ),
                        )
urlpatterns += patterns('',
                        url(r'^ajax/coupon/', include('apps.ajax.urls', ), ),
                        url(r'^ajax/slides/', include('apps.ajax.urls', ), ),
                        url(r'^ajax/order/', include('apps.ajax.urls', ), ),
                        url(r'^ajax/callback/', include('apps.ajax.urls', ), ),
                        url(r'^ajax/feedback/', include('apps.ajax.urls', ), ),
                        url(r'^ajax/timezone/', include('apps.ajax.urls', ), ),
                        url(r'^ajax/geoip/', include('apps.ajax.urls', ), ),
                        )
#Opinion - Мнение - Отыв
urlpatterns += patterns('',
                        url(regex=r'^opinion/',
                            view=include(arg='apps.opinion.urls',
                                         namespace='opinion_en', ),
                            ),
                        url(regex=ur'^отзыв/',
                            view=include(arg='apps.opinion.urls',
                                         namespace='opinion_ru', ),
                            ),
                        url(regex=r'^opinions/',
                            view=include(arg='apps.opinion.urls',
                                         namespace='opinions_en', ),
                            ),
                        url(regex=ur'^отзывы/',
                            view=include(arg='apps.opinion.urls',
                                         namespace='opinions_ru', ),
                            ),
                        )
#Delivery
urlpatterns += patterns('',
                        url(regex=r'^delivery/',
                            view=include(arg='apps.delivery.urls',
                                         namespace='delivery', ),
                            ),
                        )
#!!!===================== Static media ======================
from os.path import abspath, dirname, join, isfile
PROJECT_PATH = abspath(dirname(__name__, ), )
path = lambda base: abspath(
    join(
        PROJECT_PATH, base,
    ).replace('\\', '/')
)
if not isfile(path('server.key', ), ):
    from sys import platform
    if platform == 'win32':
        urlpatterns += patterns('django.views.static',
                                url(r'^media/(?P<path>.*)$', 'serve',
                                    {'document_root': path('media', ),
                                     'show_indexes': True, },
                                    ),
                                )
    elif platform == 'linux2':
        urlpatterns += patterns('django.views.static',
                                url(r'^media/(?P<path>.*)$', 'serve',
                                    {'document_root': path('media', ),
                                     'show_indexes': True, },
                                    ),
                                )
    # if sys.platform.startswith('freebsd'):
from settings import DEBUG
if DEBUG:
    from debug_toolbar import urls
    urlpatterns += patterns('',
                            url(r'^__debug__/',
                                include(urls), ),
                            )
#    import debug_toolbar_htmltidy
#    urlpatterns += patterns('',
#                            url(r'^', include('debug_toolbar_htmltidy.urls')),
#                            )
#!!!===================== Django Social Auth ======================
urlpatterns += patterns('apps.root.views',
                        url(r'social/index/$', 'root_page',
                            {'template_name': u'social_index.jinja2', },
                            name='social_index_page', ),
                        url(r'login/error/$', 'root_page',
                            {'template_name': u'login_error.jinja2', },
                            name='login_error', ),
                        url(r'social/', include('social.apps.django_app.urls',
                                                namespace='social', ),
                            ),
                        )
#!!!===================== Django Userena - Accounts - uMessages======================
urlpatterns += patterns('',
                        url(r'^accounts/', include('userena.urls'),
                            ),
                        url(r'^messages/', include('userena.contrib.umessages.urls'),
                            ),
                        )
#!!!===================== Статические страницы ======================================
urlpatterns += patterns('apps.static.views',
                        url(ur'^(?P<static_page_url>[а-яА-Яa-zA-ZёЁїЇіІґҐєЄ0-9_.-]+)/$',
                            'show_static_page',
                            {'template_name': u'static_page.jinja2', },
                            name='show_static_page', ),
                        )


#urlpatterns += patterns('',
#    url(r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
#        {'document_root': 'C:/Python27/Lib/site-packages/django/contrib/admin'}),
#)
#Static_sitemaps
#urlpatterns = patterns('',
#        url(r'^sitemap.xml', include('static_sitemaps.urls')),
#)

from apps.utils.sitemaps import CategoryViewSitemap, ProductViewSitemap, StaticViewSitemap


sitemaps = {
    'Category': CategoryViewSitemap,
    'Product': ProductViewSitemap,
    'Static': StaticViewSitemap,
}

#from apps.product.models import Category


#info_dict_Category = {
#    'queryset': Category.objects.all(),
#    'date_field': 'updated_at',
##    'protocol': 'http',
#}
#from django.contrib.sitemaps import GenericSitemap


#sitemaps = {
#    'Category': GenericSitemap(info_dict_Category, priority=0.9, changefreq='weekly', )
#}

#from django.contrib.sitemaps.views import index, sitemap
#
#urlpatterns += patterns('',
#                        url(r'^sitemap\.xml$', index,
##                            'django.contrib.sitemaps.views.sitemap',
#                            {'sitemaps': sitemaps}, ),
#                        url(r'^sitemap-(?P<section>.+)\.xml$',
#                            sitemap, {'sitemaps': sitemaps}, ), )

from django.contrib.sitemaps import views as sitemaps_views
from django.views.decorators.cache import cache_page

urlpatterns += patterns('',
                        url(r'^sitemap\.xml$',
                            cache_page(7200)(sitemaps_views.index),
                            {'sitemaps': sitemaps, 'sitemap_url_name': 'sitemaps'}),
                        url(r'^sitemap-(?P<section>.+)\.xml$',
                            cache_page(7200)(sitemaps_views.sitemap),
                            {'sitemaps': sitemaps}, name='sitemaps'),
                        )

#handler404 = 'apps.handlers.views.handler404'
