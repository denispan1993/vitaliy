# coding=utf-8
__author__ = 'user'

from django.core.management.base import BaseCommand


class Command(BaseCommand, ):
    def handle(self, *args, **options):
        from apps.discount.models import Action
        from apps.product.models import Product
        action_active = Action.objects.active()
        print action_active
        for action in action_active:
            print action
            products_of_action = action.action_set.all()
            print products_of_action
        Product.objects.filter(is_availability=2, ).update(is_availability=5, )
        Product.objects.filter(is_availability=3, ).update(is_availability=2, )
        Product.objects.filter(is_availability=5, ).update(is_availability=3, )
