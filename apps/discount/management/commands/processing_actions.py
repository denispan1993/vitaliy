# coding=utf-8
__author__ = 'user'

from django.core.management.base import BaseCommand


class Command(BaseCommand, ):
    def handle(self, *args, **options):
        from datetime import datetime
        print datetime.now()
        from apps.product.models import Category
        try:
            action_category = Category.objects.get(url=u'акции', )
        except Category.DoesNotExist:
            action_category = None
        from apps.discount.models import Action
        action_active = Action.objects.active()
        if action_active:
            print 'Action - ACTIVE:', action_active
            for action in action_active:
                products_of_action = action.product_in_action.all()
                print 'All products:', products_of_action
                # print action
                """
                    Если акция с автостартом,
                    то мы еЁ стартуем.
                """
                if action.auto_start:
                    products_of_action = action.product_in_action.not_in_action()
                    print products_of_action
                    for product in products_of_action:
                        print 'Add product to Action: ', product
                        """
                            Помечает товар как учавствующий в акции
                        """
                        product.category.add(action_category, )
                        product.in_action = True
                        # """
                        #     Меняем местами акционную нынешнюю
                        # """
                        # price = product.regular_price
                        # product.regular_price = product.price
                        # product.price = price
                        product.save()

        action_not_active = Action.objects.not_active()
        if action_not_active:
            print 'Action - NOT ACTIVE:', action_not_active
            for action in action_not_active:
                products_of_action = action.product_in_action.all()
                print 'All products:', products_of_action
                # print action
                """
                    Если акция с авто окончанием,
                    то заканчиваем еЁ.
                """
                if action.auto_end:
                    products_of_action = action.product_in_action.in_action()
                    print products_of_action
                    for product in products_of_action:
                        print 'Del product from Action: ', product
                        """
                            Помечает товар как не учавствующий в акции
                        """
                        product.category.remove(action_category, )
                        product.in_action = False
                        # """
                        #     Меняем местами нынешнюю и акционные цены местами
                        # """
                        # price = product.price
                        # product.price = product.regular_price
                        # if action.auto_del_action_price:
                        #     product.regular_price = 0
                        # else:
                        #     product.regular_price = price
                        if action.auto_del_action_from_product:
                            print action.auto_del_action_from_product
                            print 'remove'
                            product.action.remove(action, )
                        product.save()
                    if action.auto_del:
                        action.deleted = True
                        action.save()
            # from apps.product.models import Product
            # Product.objects.filter(is_availability=2, ).update(is_availability=5, )
            # Product.objects.filter(is_availability=3, ).update(is_availability=2, )
            # Product.objects.filter(is_availability=5, ).update(is_availability=3, )

        all_actions_products = action_category.products.all()
        if len(all_actions_products) != 0:
            action_category.is_active = True
        else:
            action_category.is_active = False
        action_category.save()
