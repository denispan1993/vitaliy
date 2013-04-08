# coding=utf-8
#from django.conf.urls import patterns, include, url
from coffin.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
from apps.root.views import root_page
from apps.product.views import show_category, show_product
from apps.cart.views import show_cart
from apps.ajax.views import resolution, cookie

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'proj.views.home', name='home'),
    url(r'^$', root_page,
        {'template_name': u'../apps/root/templates/root.jinja2.html', },
        name='root_page', ),
    # url(r'^proj/', include('proj.foo.urls')),
    url(ur'^(?P<category_url>[а-яА-Яa-zA-ZёЁїЇіІґҐєЄ0-9_.-]+)/[кc](?P<id>\d{6})/$', show_category,
        {'template_name': u'category/show_category.jinja2.html', },
        name='show_category', ),
    url(ur'^(?P<product_url>[а-яА-Яa-zA-ZёЁїЇіІґҐєЄ0-9_.-]+)/[пp](?P<id>\d{6})/$', show_product,
        {'template_name': u'product/show_product.jinja2.html', },
        name='show_product', ),
    url(ur'^корзина/$', show_cart,
        {'template_name': u'show_cart.jinja2.html', },
        name='show_cart', ),

    url(r'^ajax/resolution/$', resolution,
#       {'template_name': u'product/show_product.jinja2.html', },
        name='ajax_resolution', ),
    url(r'^ajax/cookie/$', cookie,
        name='ajax_cookie', ),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls', ), ),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls, ), ),
)

#!!!===================== Static media ======================
from django.conf import settings
if settings.DEBUG:
    import sys
    if sys.platform == 'win32':
        urlpatterns += patterns('django.views.static',
                                url(r'^media/(?P<path>.*)$', 'serve',
                                    {'document_root': 'C:/Shop/Media',
                                     'show_indexes': True, },
                                    ),
                                )
    elif sys.platform == 'linux2':
        urlpatterns += patterns('django.views.static',
                                url(r'^media/(?P<path>.*)$', 'serve',
                                    {'document_root': '/home/user/Proj/Shop/Media',
                                    'show_indexes': True, },
                                    ),
                                )
#!!!===================== Django Social Auth ======================
urlpatterns += patterns('',
                        url(r'social/index/$', root_page,
                            {'template_name': u'social_index.jinja2.html', },
                            name='social_index_page', ),
                        url(r'login/error/$', root_page,
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
#urlpatterns += patterns('',
#    url(r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
#        {'document_root': 'C:/Python27/Lib/site-packages/django/contrib/admin'}),
#)
