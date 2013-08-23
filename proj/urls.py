# coding=utf-8
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
#from apps.root.views import root_page
#from apps.product.views import show_category, show_product
#from apps.cart.views import show_cart
#from apps.ajax.views import resolution, cookie

urlpatterns = patterns('apps',
    # Examples:
    # url(r'^$', 'proj.views.home', name='home'),
    url(r'^$', 'root.views.root_page',
        {'template_name': u'index.jinja2.html', },
        name='root_page', ),
    # url(r'^proj/', include('proj.foo.urls')),
    url(ur'^категории/$', 'product.views.show_basement_category',
        {'template_name': u'category/show_basement_category.jinja2.html', },
        name='show_basement_category', ),
    url(ur'^(?P<category_url>[а-яА-Яa-zA-ZёЁїЇіІґҐєЄ0-9_.-]+)/[кc](?P<id>\d{6})/$', 'product.views.show_category',
        {'template_name': u'category/show_category.jinja2.html', },
        name='show_category', ),
    url(ur'^(?P<product_url>[а-яА-Яa-zA-ZёЁїЇіІґҐєЄ0-9_.-]+)/[пp](?P<id>\d{6})/$', 'product.views.show_product',
        {'template_name': u'product/show_product.jinja2.html', },
        name='show_product', ),
    url(ur'^корзина/$', 'cart.views.show_cart',
        {'template_name': u'show_cart.jinja2.html', },
        name='show_cart', ),
    url(ur'^корзина/пересчитать/$', 'cart.views.recalc_cart',
        name='recalc_cart', ),
    url(ur'^корзина/заказ/$', 'cart.views.show_order',
        {'template_name': u'show_order.jinja2.html', },
        name='show_order', ),
    url(ur'^корзина/заказ/принят/$', 'cart.views.show_order_success',
        {'template_name': u'show_order_success.jinja2.html', },
        name='show_order_success', ),
    url(ur'^корзина/order/$', 'cart.views.show_order',
        {'template_name': u'show_order.jinja2.html', },
        name='show_order', ),
    url(r'^cart/$', 'cart.views.show_cart',
        {'template_name': u'show_cart.jinja2.html', },
        name='show_cart', ),
    url(ur'^cart/заказ/$', 'cart.views.show_order',
        {'template_name': u'show_order.jinja2.html', },
        name='show_order', ),
    url(r'^cart/order/$', 'cart.views.show_order',
        {'template_name': u'show_order.jinja2.html', },
        name='show_order', ),
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
#Admin
urlpatterns += (
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls', ), ),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls, ), ),
)

#!!!===================== Static media ======================
import os
PROJECT_PATH = os.path.abspath(os.path.dirname(__name__), )
ROOT = PROJECT_PATH
path = lambda base: os.path.abspath(
    os.path.join(
        PROJECT_PATH, base
    ).replace('\\', '/')
)

from django.conf import settings
if settings.DEBUG:
    import sys
    if sys.platform == 'win32':
        urlpatterns += patterns('django.views.static',
                                url(r'^media/(?P<path>.*)$', 'serve',
                                    {'document_root': path('media', ),
                                     'show_indexes': True, },
                                    ),
                                )
    elif sys.platform == 'linux2':
        urlpatterns += patterns('django.views.static',
                                url(r'^media/(?P<path>.*)$', 'serve',
                                    {'document_root': path('media', ),
                                    'show_indexes': True, },
                                    ),
                                )
#!!!===================== Django Social Auth ======================
urlpatterns += patterns('apps.root.views',
                        url(r'social/index/$', 'root_page',
                            {'template_name': u'social_index.jinja2.html', },
                            name='social_index_page', ),
                        url(r'login/error/$', 'root_page',
                            {'template_name': u'login_error.jinja2.html', },
                            name='login_error', ),
                        url(r'social/', include('social_auth.urls'),
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
                        url(ur'^(?P<static_page_url>[а-яА-Яa-zA-ZёЁїЇіІґҐєЄ0-9_.-]+)/$', 'show_static_page',
                        {'template_name': u'static_page.jinja2.html', },
                        name='show_category', ),
                        )


#urlpatterns += patterns('',
#    url(r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
#        {'document_root': 'C:/Python27/Lib/site-packages/django/contrib/admin'}),
#)
