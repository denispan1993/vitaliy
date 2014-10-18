# coding=utf-8
__author__ = 'user'

from django.core.management.base import BaseCommand


class Command(BaseCommand, ):
    def handle(self, *args, **options):
        from apps.discount.models import Action
        action_active = Action.objects.active()
        print action_active
        for action in action_active:
            print action
            """
                Если акция с автостартом,
                то мы еЁ стартуем.
            """
            if action.auto_start:
                products_of_action = action.action_set.not_in_action()
                print products_of_action
                for product in products_of_action:
                    print product
                    """
                        Помечаеит товар как учавствующий в акции
                    """
                    product.in_action = True
                    """
                        Меняем местами акционную нынешнюю
                    """
                    price = product.regular_price
                    product.regular_price = product.price
                    product.price = price
                    product.save()

        action_not_active = Action.objects.not_active()
        print action_not_active
        for action in action_not_active:
            print action
            """
                Если акция с авто окончанием,
                то заканчиваем еЁ.
            """
            if action.auto_end:
                products_of_action = action.action_set.in_action()
                print products_of_action
                for product in products_of_action:
                    print product
                    """
                        Помечаеит товар как не учавствующий в акции
                    """
                    product.in_action = True
                    """
                        Меняем местами нынешнюю и акционные цены местами
                    """
                    price = product.price
                    product.price = product.regular_price
                    if action.auto_del_action_price:
                        product.regular_price = 0
                    else:
                        product.regular_price = price
                    product.action.delete(action, )
                    product.save()
                if action.auto_del:
                    action.deleted = True
                    action.save()
        # from apps.product.models import Product
        # Product.objects.filter(is_availability=2, ).update(is_availability=5, )
        # Product.objects.filter(is_availability=3, ).update(is_availability=2, )
        # Product.objects.filter(is_availability=5, ).update(is_availability=3, )