# -*- coding: utf-8 -*-
from django.conf.urls import include, url
from django.conf.urls.static import static

from django.contrib.sitemaps import views as sitemaps_views
from django.views.decorators.cache import cache_page
from django.views.static import serve
from os.path import abspath, dirname, join, isfile
from sys import platform

from applications.root.views import root_page
from applications.product.views import show_basement_category, show_category, show_product
from applications.comment.views import comment_add, comment_add_successfully
from applications.ajax.comment import comment_change
from applications.currency.views import currency_change
from applications.search.views import search_page
from applications.ajax.views import resolution, cookie, sel_country, product_to_cart
from applications.static.views import show_static_page
from applications.utils.sitemaps import CategoryViewSitemap, ProductViewSitemap, StaticViewSitemap

import proj.settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

# from filebrowser.sites import site
''' Admin '''
urlpatterns = [
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls', ), ),
    # url(r'^admin/filebrowser/', include(site.urls, ), ),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls, ), ),
    url(r'^captcha/', include('applications.utils.captcha.urls', ), ),
    url(regex=r'^redirect/',
        view=include(arg='applications.delivery2.urls',
                     namespace='delivery_old'), ),
]

urlpatterns += [url(regex=r'^$',
                    view=root_page,
                    kwargs={'template_name': u'root.jinja2', },
                    name='root_page', ),
                url(regex=r'^категории/$',
                    view=show_basement_category,
                    kwargs={'template_name': u'category/show_basement_category.jinja2', },
                    name='show_basement_category', ),
                url(regex=r'^(?P<category_url>[а-яА-Яa-zA-ZёЁїЇіІґҐєЄ0-9_.-]+)/[кc](?P<id>\d{6})/$',
                    view=show_category,
                    kwargs={'template_name': u'category/category.jinja2', },
                    name='show_category', ),
                url(regex=r'^(?P<product_url>[а-яА-Яa-zA-ZёЁїЇіІґҐєЄ0-9_.-]+)/[пp](?P<id>\d{6})/$',
                    view=show_product,
                    kwargs={'template_name': u'product/product.jinja2', },
                    name='show_product', ),
                        ]
"""
    Раздел:
        Комментариев.
"""
urlpatterns += [
    url(regex=r'^(?P<product_url>[а-яА-Яa-zA-ZёЁїЇіІґҐєЄ0-9_.-]+)/[пp](?P<id>\d{6})/комментарий/добавить/$',
        view=comment_add,
        kwargs={'template_name': u'show_comment_add.jinja2',
                'comment_id': None, },
        name='show_comment_add', ),
    url(regex=r'^(?P<product_url>[а-яА-Яa-zA-ZёЁїЇіІґҐєЄ0-9_.-]+)/[пp](?P<id>\d{6})/комментарий/(?P<comment_id>\d{6})/добавить/$',
        view=comment_add,
        kwargs={'template_name': u'show_comment_add.jinja2', },
        name='show_comment_add', ),
    url(regex=r'^(?P<product_url>[а-яА-Яa-zA-ZёЁїЇіІґҐєЄ0-9_.-]+)/[пp](?P<id>\d{6})/комментарий/добавлен/успешно/$',
        view=comment_add_successfully,
        kwargs={'template_name': u'show_comment_add_successfully.jinja2', },
        name='comment_add_successfully', ), ]

""" Изменение комментария """
urlpatterns += [
    url(regex=r'^ajax/comment/change/$',
        view=comment_change,
        name='ajax_comment_change', ), ]

"""
    Раздел:
        Корзины.
"""

urlpatterns += [url(regex=r'^корзина/',
                    view=include(arg='applications.cart.urls',
                                 namespace='cart', ),
                    ), ]

urlpatterns += [url(regex=r'^заказ/',
                    view=include(arg='applications.cart.urls',
                                 namespace='order', ),
                    ), ]


urlpatterns += [url(regex=r'^Currency/Change/$',
                    view=currency_change,
                    name='currency_change', ),
                url(regex=r'^Валюта/Изменение/$',
                    view=currency_change,
                    name='currency_change', ), ]


urlpatterns += [url(regex=r'^оплата/',
                    view=include(arg='applications.payment.urls',
                                 namespace='payment', ),
                    ), ]

# Капча
# urlpatterns += patterns(url(r'^captcha/', include('applications.utils.captcha.urls', ), ), )

''' Admin panel '''
""" Админ панель Заказов. """
urlpatterns += [url(regex=r'^админ/',
                    view=include(arg='applications.adminSite.urls',
                                 namespace='admin_page', ), ), ]
''' Search '''
urlpatterns += [url(regex=r'^поиск/$',
                    view=search_page,
                    kwargs={'query': None,
                            'template_name': u'category/show_category.jinja2', },
                    name='show_search', ),
                url(regex=r'^поиск/(?P<query>\d+)$',
                    view=search_page,
                    kwargs={'template_name': u'category/show_category.jinja2', },
                    name='show_search', ),
                url(regex=r'^search/$',
                    view=search_page,
                    kwargs={'query': None,
                            'template_name': u'category/show_category.jinja2', },
                    name='show_search', ),
                url(regex=r'^search/(?P<query>\d+)$',
                    view=search_page,
                    kwargs={'template_name': u'category/show_category.jinja2', },
                    name='show_search', ), ]

''' Календарь'''
urlpatterns += [url(regex=r'^календарь/',
                    view=include(arg='applications.mycalendar.urls',
                                 namespace='calendar', ),
                    ), ]

''' Ajax '''
urlpatterns += [url(regex=r'^ajax/resolution/$',
                    view=resolution,
                    name='ajax_resolution', ),
                url(regex=r'^ajax/cookie/$',
                    view=cookie,
                    name='ajax_cookie', ),
                url(regex=r'^ajax/country/$',
                    view=sel_country,
                    name='ajax_country', ),
                url(regex=r'^ajax/product_to_cart/$',
                    view=product_to_cart,
                    name='ajax_product_to_cart', ), ]

urlpatterns += [url(regex=r'^ajax/coupon/', view=include('applications.ajax.urls', ), ),
                url(regex=r'^ajax/slides/', view=include('applications.ajax.urls', ), ),
                url(regex=r'^ajax/order/', view=include('applications.ajax.urls', ), ),
                url(regex=r'^ajax/callback/', view=include('applications.ajax.urls', ), ),
                url(regex=r'^ajax/feedback/', view=include('applications.ajax.urls', ), ),
                url(regex=r'^ajax/timezone/', view=include('applications.ajax.urls', ), ),
                url(regex=r'^ajax/geoip/', view=include('applications.ajax.urls', ), ), ]

''' Opinion - Мнение - Отыв '''
urlpatterns += [url(regex=r'^opinion/',
                    view=include(arg='applications.opinion.urls',
                                 namespace='opinion_en', ), ),
                url(regex=r'^отзыв/',
                    view=include(arg='applications.opinion.urls',
                                 namespace='opinion_ru', ), ),
                url(regex=r'^opinions/',
                    view=include(arg='applications.opinion.urls',
                                 namespace='opinions_en', ), ),
                url(regex=r'^отзывы/',
                    view=include(arg='applications.opinion.urls',
                                 namespace='opinions_ru', ), ), ]
''' Delivery '''
urlpatterns += [url(regex=r'^delivery/',
                    view=include(arg='applications.delivery2.urls',
                                 namespace='delivery', ), ),
                url(regex=r'^message/',
                    view=include(arg='applications.delivery2.urls',
                                 namespace='message', ), ),
                url(regex=r'^email/',
                    view=include(arg='applications.delivery2.urls',
                                 namespace='email', ), ), ]
''' Bitrix '''
urlpatterns += [url(regex=r'^bitrix/',
                    view=include(arg='applications.bitrix.urls',
                                 namespace='bitrix', ), ), ]

# !!!===================== Static media ======================
PROJECT_PATH = abspath(dirname(__name__, ), )
path = lambda base: abspath(
    join(
        PROJECT_PATH, base,
    ).replace('\\', '/')
)
if not isfile(path('server.key', ), ):
    if platform == 'win32':
        urlpatterns += [url(regex=r'^media/(?P<path>.*)$', view=serve,
                            kwargs={'document_root': path('media', ),
                                    'show_indexes': True, }, ), ]
    elif platform == 'linux':
        urlpatterns += [url(regex=r'^media/(?P<path>.*)$', view=serve,
                            kwargs={'document_root': path('media', ),
                                    'show_indexes': True, }, ), ]  # \
                       # + static(proj.settings.MEDIA_URL, document_root=proj.settings.MEDIA_ROOT)

    # if sys.platform.startswith('freebsd'):

if proj.settings.DEBUG:
    from debug_toolbar import urls
    urlpatterns += [url(regex=r'^__debug__/', view=include(urls), ), ]
#    import debug_toolbar_htmltidy
#    urlpatterns += patterns('',
#                            url(r'^', include('debug_toolbar_htmltidy.urls')),
#                            )
# !!!===================== Django Social Auth ======================
urlpatterns += [url(regex='social/index/$', view=root_page,
                    kwargs={'template_name': u'social_index.jinja2', },
                    name='social_index_page', ),
                url(regex=r'login/error/$', view=root_page,
                    kwargs={'template_name': u'login_error.jinja2', },
                    name='login_error', ),
                url(regex=r'social/',
                    view=include('social.apps.django_app.urls',
                                 namespace='social', ), ), ]
# !!!===================== Django Userena - Accounts - uMessages======================
urlpatterns += [url(regex=r'^accounts/', view=include('userena.urls'), ),
                url(regex=r'^messages/', view=include('userena.contrib.umessages.urls'), ), ]
# !!!===================== Статические страницы ======================================
urlpatterns += [url(regex=r'^(?P<static_page_url>[а-яА-Яa-zA-ZёЁїЇіІґҐєЄ0-9_.-]+)/$',
                    view=show_static_page,
                    kwargs={'template_name': u'static_page.jinja2', },
                    name='show_static_page', ), ]

sitemaps = {
    'Category': CategoryViewSitemap,
    'Product': ProductViewSitemap,
    'Static': StaticViewSitemap,
}

urlpatterns += [url(regex=r'^sitemap\.xml$',
                    view=cache_page(7200)(sitemaps_views.index),
                    kwargs={'sitemaps': sitemaps, 'sitemap_url_name': 'sitemaps'}),
                url(regex=r'^sitemap-(?P<section>.+)\.xml$',
                    view=cache_page(7200)(sitemaps_views.sitemap),
                    kwargs={'sitemaps': sitemaps}, name='sitemaps'), ]

urlpatterns += [url(regex=r'^yandex/',
                    view=include(arg='applications.yandex.urls',
                                 namespace='yandex'), ), ]

# handler404 = 'applications.handlers.views.handler404'
