# -*- coding: utf-8 -*-
__author__ = 'AlexStarov'

from django.core.management.base import BaseCommand


class Command(BaseCommand, ):
    from optparse import make_option
    option_list = BaseCommand.option_list + (
        make_option('-id', '-pk', '--delivery_id', '--delivery_pk',
                    action='store', type='int', dest='delivery_pk',
                    help=''),
        make_option('-t', '--delivery_test', '--test',
                    action='store_true', dest='delivery_test',
                    help=''),
        make_option('-g', '--delivery_general', '--general',
                    action='store_true', dest='delivery_test',
                    help=''),
    )
    #self.verbosity = int(options.get('verbosity'))
    #def add_arguments(self, parser):
    #    parser.add_argument('delivery_id', nargs='+', type=int)

    def handle(self, *args, **options):
        from apps.delivery.models import Delivery
        try:
            deliveryes = Delivery.objects.filter(delivery_test=True, )
        except Delivery.DoesNotExist:
            deliveryes = None
        else:
            from apps.delivery.models import EmailMiddleDelivery
            for delivery in deliveryes:
                print delivery
                try:
                    aaa=EmailMiddleDelivery.objects.\
                        get(delivery=delivery, updated_at__lte=delivery.updated_at, )
                    print aaa, delivery.updated_at
                except:
                    """ Создаем ссылочку на отсылку рассылки """
                    email_middle_delivery = EmailMiddleDelivery()
                    email_middle_delivery.delivery = delivery
                    email_middle_delivery.delivery_test_send = True
                    email_middle_delivery.delivery_send = False
                    email_middle_delivery.save()
                    """ Отсылаем тестовое письмо """
                    from django.utils.html import strip_tags

                    from django.core.mail import get_connection
                    backend = get_connection(backend='django.core.mail.backends.smtp.EmailBackend',
                                             fail_silently=False, )
                    from django.core.mail import EmailMultiAlternatives
                    from proj.settings import Email_MANAGER
                    msg = EmailMultiAlternatives(subject='test - %s' % delivery.subject,
                                                 body=strip_tags(delivery.html, ),
                                                 from_email=u'site@keksik.com.ua',
                                                 to=[Email_MANAGER, ],
                                                 connection=backend, )
                    msg.attach_alternative(content=delivery.html,
                                           mimetype="text/html", )
                    msg.content_subtype = "html"
                    msg.send(fail_silently=False, )

        try:
            deliveryes = Delivery.objects.filter(delivery_test=False, )
        except Delivery.DoesNotExist:
            deliveryes = None
        else:
            from apps.authModel.models import Email
            from apps.delivery.models import EmailForDelivery
            for delivery in deliveryes:
                try:

                    aaa=EmailMiddleDelivery.objects.\
                        get(delivery=delivery, updated_at__lte=delivery.updated_at, )
                    print aaa, delivery.updated_at
                except:
                    email_middle_delivery = EmailMiddleDelivery()
                    email_middle_delivery.delivery = delivery
                    email_middle_delivery.delivery_test_send = False
                    email_middle_delivery.delivery_send = True
                    email_middle_delivery.save()
                    """ Создаем указатели на E-Mail адреса рассылки """
                    try:
                        emails = Email.objects.all()
                    except Email.DoesNotExist:
                        emails = None
                    """ Здесь нужно помудрить с коммитом """
                    for real_email in emails:
                        email = EmailForDelivery()
                        email.delivery = email_middle_delivery
                        email.email = real_email
                        """ | """
                        email.save()
                        from django.utils.html import strip_tags

                        from django.core.mail import get_connection
                        backend = get_connection(backend='django.core.mail.backends.smtp.EmailBackend',
                                                 fail_silently=False, )
                        from django.core.mail import EmailMultiAlternatives
                        from proj.settings import Email_MANAGER
                        msg = EmailMultiAlternatives(subject=delivery.subject,
                                                     body=strip_tags(delivery.html, ),
                                                     from_email=u'site@keksik.com.ua',
                                                     to=[real_email.email, ],
                                                     connection=backend, )
                        msg.attach_alternative(content=delivery.html,
                                               mimetype="text/html", )
                        msg.content_subtype = "html"
                        print real_email.email
                        #try:
                        #    # msg.send(fail_silently=False, )
                        #except Exception as inst:
                        #    print type(inst, )
                        #    print inst.args
                        #    print inst
                        # else:
                        #    email.send
                        #    email.save()


                #try:
                #    """ Берем 10 E-Mail адресов на которые мы еще не отсылали данную рассылку """
                #    emails = EmailForDelivery.objects.filter(delivery=email_middle_delivery,
                #                                             send=False, )[10]
                #except EmailForDelivery.DoesNotExist:
                #    """ E-Mail адреса в этой рассылке закончились """
                #    emails = None
                #else:
                #    emails = ', '.join(emails, )
                #    """ Отсылаем E-Mail на 10 адресатов """


def hernya():
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
                """ Включаем галочку 'Учавствует в акции' всем продуктам которые внесены в акцию
                    исключая продукты 'отсутсвующие на складе' """
                products_of_action = action.product_in_action.exclude(is_availability=4, )
                if len(products_of_action, ) > 0:
                    print 'Product auto_start:', products_of_action
                    for product in products_of_action:
                        """ Помечает товар как учавствующий в акции """
                        product.in_action = True
                        """ Добавляем категорию 'Акция' в товар """
                        product.category.add(action_category, )
                        product.save()
                """ Удаляем товары учавствующие в активной акции но при этом 'отсутсвующие на складе' """
                products_remove_from_action = action.product_in_action.exclude(is_availability__lt=4, )
                if len(products_of_action, ) > 0:
                    print 'Product auto_start:', products_of_action
                    for product in products_remove_from_action:
                        """ Помечает товар как учавствующий в акции """
                        product.in_action = False
                        """ Добавляем категорию 'Акция' в товар """
                        product.category.remove(action_category, )
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
                if len(products_of_action, ) > 0:
                    print 'Product auto_end:', products_of_action
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
                            product.action.remove(action, )
                        product.save()
                    if action.auto_del:
                        action.deleted = True
                        action.save()
        # from apps.product.models import Product
        # Product.objects.filter(is_availability=2, ).update(is_availability=5, )
        # Product.objects.filter(is_availability=3, ).update(is_availability=2, )
        # Product.objects.filter(is_availability=5, ).update(is_availability=3, )

    """ Убираем галочку 'участвует в акции' всем продуктам у которых она почемуто установлена,
     но при этом отсутвует хоть какая то акция """
    from apps.product.models import Product
    products = Product.objects.filter(in_action=True, action=None, ).update(in_action=False, )
    print 'Товары удаленные из акции по причине вывода их из акции: ', products

    """ Убираем галочку 'участвует в акции' всем продуктам которые отсутсвуют на складе """
    products = Product.objects.filter(in_action=True, is_availability=4, ).update(in_action=False, )
    print 'Товары удаленные из акции по причине отсутсвия на складе: ', products

    """ Делаем активной акционную категорию, если есть хоть один акционный товар """
    all_actions_products = action_category.products.all()
    if len(all_actions_products) != 0 and not action_category.is_active:
        action_category.is_active = True
        action_category.save()
    elif len(all_actions_products) == 0 and action_category.is_active:
        action_category.is_active = False
        action_category.save()