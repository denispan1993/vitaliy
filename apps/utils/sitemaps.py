# coding=utf-8
__author__ = 'Alex Starov'

from django.contrib.sitemaps import Sitemap


class CategoryViewSitemap(Sitemap, ):
    protocol = 'http'
    priority = 0.7
    changefreq = 'monthly'

    def items(self, ):
        from apps.product.models import Category
        return Category.objects.all()

    def location(self, obj, ):
        return obj.get_absolute_url()

    def lastmod(self, obj, ):
        return obj.updated_at


class ProductViewSitemap(Sitemap, ):
    protocol = 'http'
    priority = 0.5
    changefreq = 'weekly'

    def items(self, ):
        from apps.product.models import Product
        return Product.objects.all()

    def location(self, obj, ):
        return obj.get_absolute_url()

    def lastmod(self, obj, ):
        return obj.updated_at


class StaticViewSitemap(Sitemap, ):
    protocol = 'http'
    priority = 0.9
    changefreq = 'weekly'

    def items(self, ):
        from apps.static.models import Static
        return Static.objects.all()

    def location(self, obj, ):
        return obj.get_absolute_url()

    def lastmod(self, obj, ):
        return obj.updated_at
