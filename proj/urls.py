# coding=utf-8
# from django.conf.urls import patterns, include, url
try:
    from django.conf.urls import patterns, include, url
except ImportError:  # django < 1.4
    from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

#Admin
urlpatterns = patterns(
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls', ), ),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls, ), ),
)

#from apps.root.views import root_page
#from apps.product.views import show_category, show_product
#from apps.cart.views import show_cart
#from apps.ajax.views import resolution, cookie

urlpatterns += patterns('apps',
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
        {'template_name': u'category/show_content_center.jinja2.html', },
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
#    url(r'^Currency/Change/$', 'currency.views.currency_change',
#        name='currency_change', ),
#    url(ur'^Валюта/Изменение/$', 'currency.views.currency_change',
#        name='currency_change', ),

)
#Search
urlpatterns += patterns('apps.search.views',
                        url(ur'^поиск/$', 'search_page',
                            {'query': None,
                             'template_name': u'category/show_content_center.jinja2.html', },
                            name='show_search', ),
                        url(ur'^поиск/(?P<query>\d+)$', 'search_page',
                            {'template_name': u'category/show_content_center.jinja2.html', },
                            name='show_search', ),
                        url(r'^search/$', 'search_page',
                            {'query': None,
                            'template_name': u'category/show_content_center.jinja2.html', },
                            name='show_search', ),
                        url(r'^search/(?P<query>\d+)$', 'search_page',
                            {'template_name': u'category/show_content_center.jinja2.html', },
                            name='show_search', ),
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
#!!!===================== Static media ======================
from os.path import abspath, dirname, join, isfile
PROJECT_PATH = abspath(dirname(__name__, ), )
path = lambda base: abspath(
    join(
        PROJECT_PATH, base,
    ).replace('\\', '/')
)
if not isfile(path('server.key', ), ):
    from settings import DEBUG
    if DEBUG:
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
                        url(ur'^(?P<static_page_url>[а-яА-Яa-zA-ZёЁїЇіІґҐєЄ0-9_.-]+)/$',
                            'show_static_page',
                            {'template_name': u'static_page.jinja2.html', },
                            name='show_category', ),
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
                            cache_page(86400)(sitemaps_views.index),
                            {'sitemaps': sitemaps, 'sitemap_url_name': 'sitemaps'}),
                        url(r'^sitemap-(?P<section>.+)\.xml$',
                            cache_page(86400)(sitemaps_views.sitemap),
                            {'sitemaps': sitemaps}, name='sitemaps'),
                        )