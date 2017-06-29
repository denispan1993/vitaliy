# -*- coding: utf-8 -*-
from proj.celery import celery_app
from datetime import datetime
from logging import getLogger
from celery.utils.log import get_task_logger

from applications.product.models import Category, Product
from .models import Action

__author__ = 'AlexStarov'

logger = get_task_logger(__name__)
std_logger = getLogger(__name__)


@celery_app.task(name='discount.tasks.processing_action', )
def processing_action(*args, **kwargs):

    start = datetime.now()
    logger.info(u'Start: processing_action(*args, **kwargs)', )
    logger.info(u'message: datetime.now() {0}'.format(start), )
    std_logger.info(u'message: datetime.now() {0}'.format(start), )

    try:
        action_category = Category.objects.get(url=u'акции', )
    except Category.DoesNotExist:
        action_category = False
    """ Выключаем продукты из "АКЦИИ" срок действия акции которой уже подощёл к концу """
    action_not_active = Action.objects.not_active()
    if action_not_active:
        print('Action - NOT ACTIVE:', action_not_active, )
        for action in action_not_active:
            products_of_action = action.product_in_action.all()
            print('All products:', products_of_action, )
            """
                Если акция с авто окончанием,
                то заканчиваем еЁ.
            """
            if action.auto_end:
                products_of_action = action.product_in_action.in_action()
                if len(products_of_action, ) > 0:
                    print('Product auto_end:', products_of_action, )
                    for product in products_of_action:
                        print('Del product from Action: ', product, )
                        """
                            Помечает товар как не учавствующий в акции
                        """
                        if action_category:
                            product.category.remove(action_category, )
                        product.in_action = False
                        if action.auto_del_action_from_product:
                            if action_category:
                                product.action.remove(action, )
                        product.save()
                    if action.auto_del:
                        action.deleted = True
                        action.save()

    action_active = Action.objects.active()
    if action_active:
        print('Action - ACTIVE:', action_active, )
        for action in action_active:
            products_of_action = action.product_in_action.all()
            print('All products:', products_of_action, )
            """
                Если акция с автостартом,
                то мы еЁ стартуем.
            """
            if action.auto_start:
                """ Включаем галочку 'Учавствует в акции' всем продуктам которые внесены в акцию
                    исключая продукты 'отсутсвующие на складе' """
                products_of_action = action.product_in_action.exclude(is_availability=4, )
                if len(products_of_action, ) > 0:
                    print('Product auto_start:', products_of_action, )
                    for product in products_of_action:
                        """ Помечает товар как учавствующий в акции """
                        product.in_action = True
                        """ Добавляем категорию 'Акция' в товар """
                        if action_category:
                            product.category.add(action_category, )
                        product.save()
                """ Удаляем товары учавствующие в активной акции но при этом 'отсутсвующие на складе' """
                products_remove_from_action = action.product_in_action.exclude(is_availability__lt=4, )
                if len(products_remove_from_action, ) > 0:
                    print('Product auto_start remove:', products_remove_from_action, )
                    for product in products_remove_from_action:
                        """ Помечает товар как не учавствующий в акции """
                        product.in_action = False
                        """ Удаляем категорию 'Акция' из товара """
                        if action_category:
                            product.category.remove(action_category, )
                        product.save()

    """ Убираем галочку 'участвует в акции' всем продуктам у которых она почемуто установлена,
     но при этом отсутвует хоть какая то акция """
    products = Product.objects.filter(in_action=True, action=None, ).update(in_action=False, )
    print('Товары удаленные из акции по причине вывода их из акции: ', products, )

    """ Убираем галочку 'участвует в акции' всем продуктам которые отсутсвуют на складе """
    products = Product.objects.filter(in_action=True, is_availability=4, ).update(in_action=False, )
    print('Товары удаленные из акции по причине отсутсвия на складе: ', products, )

    """ Делаем активной акционную категорию, если есть хоть один акционный товар """
    all_actions_products = action_category.products.all()
    if len(all_actions_products) != 0 and not action_category.is_active:
        action_category.is_active = True
        action_category.save()
    elif len(all_actions_products) == 0 and action_category.is_active:
        action_category.is_active = False
        action_category.save()

    stop = datetime.now()
    logger.info(u'message: datetime.now() {0}'.format(stop), )
    logger.info(u'Stop: processing_action(*args, **kwargs): ', stop - start, )
