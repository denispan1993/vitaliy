# coding=utf-8
__author__ = 'user'

from django.core.management.base import BaseCommand


class Command(BaseCommand, ):
    def handle(self, *args, **options):
        from applications.product.models import Product
        # Product.objects.filter(is_availability=2, ).update(is_availability=5, )
        # Product.objects.filter(is_availability=3, ).update(is_availability=2, )
        # Product.objects.filter(is_availability=5, ).update(is_availability=3, )
        is_available = Product.objects.filter(is_availability=3, ).update(is_availability=2, )
        print(is_available, )
        print(len(is_available, ), )
