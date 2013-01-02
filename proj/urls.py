from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'proj.views.home', name='home'),
    url(r'^$', 'apps.root.views.root',
        {'template_name': 'root.jinja2.html', },
        name='root_page', ),
    # url(r'^proj/', include('proj.foo.urls')),
    url(r'^(?P<category_url>\w+)/c(?P<id>\d{6})/$', 'apps.products.views.show_category',
        {'tamplate_name': 'category/show_category.jinja2.html', },
        name='show_category', ),
    url(r'^(?P<product_url>\w+)/p(?P<id>\d{6})/$', 'apps.products.views.show_product',
        {'tamplate_name': 'product/show_product.jinja2.html', },
        name='show_product', ),
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
