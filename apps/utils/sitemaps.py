# -*- coding: utf-8 -*-
from django.contrib.sitemaps import Sitemap

from apps.product.models import Category, Product
from apps.static.models import Static

__author__ = 'AlexStarov'


class CategoryViewSitemap(Sitemap, ):
    protocol = 'https'
    priority = 0.7
    changefreq = 'monthly'

    def items(self, ):
        return Category.objects.all()

    def location(self, obj, ):
        return obj.get_absolute_url()

    def lastmod(self, obj, ):
        return obj.updated_at


class ProductViewSitemap(Sitemap, ):
    protocol = 'https'
    priority = 0.5
    changefreq = 'weekly'

    def items(self, ):
        return Product.objects.all()

    def location(self, obj, ):
        return obj.get_absolute_url()

    def lastmod(self, obj, ):
        return obj.updated_at


class StaticViewSitemap(Sitemap, ):
    protocol = 'https'
    priority = 0.9
    changefreq = 'weekly'

    def items(self, ):
        return Static.objects.all()

    def location(self, obj, ):
        return obj.get_absolute_url()

    def lastmod(self, obj, ):
        return obj.updated_at
