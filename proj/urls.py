from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
from apps.root.views import root_page
from apps.product.views import show_category, show_product
from apps.ajax.views import resolution

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'proj.views.home', name='home'),
    url(r'^$', root_page,
        {'template_name': u'root.jinja2.html', },
        name='root_page', ),
    # url(r'^proj/', include('proj.foo.urls')),
    url(r'^(?P<category_url>\w+)/c(?P<id>\d{6})/$', show_category,
        {'template_name': u'category/show_category.jinja2.html', },
        name='show_category', ),
    url(r'^(?P<product_url>\w+)/p(?P<id>\d{6})/$', show_product,
        {'template_name': u'product/show_product.jinja2.html', },
        name='show_product', ),

    url(r'^ajax/resolution/$', resolution,
#        {'template_name': u'product/show_product.jinja2.html', },
        name='ajax_resolution', ),


    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls', ), ),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls, ), ),
)

from django.conf import settings
if settings.DEBUG:
    urlpatterns += patterns('django.views.static',
        url(r'^media/(?P<path>.*)$', 'serve',
            {'document_root': '/home/user/Proj/Shop/Media',
             'show_indexes': True, }, ),
)

#urlpatterns += patterns('',
#    url(r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
#        {'document_root': 'C:/Python27/Lib/site-packages/django/contrib/admin'}),
#)
