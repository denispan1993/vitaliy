# -*- coding: utf-8 -*-

import os
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.forms import EmailField
from django.utils.encoding import DjangoUnicodeDecodeError

from django.core.management.base import BaseCommand

from applications.delivery.models import SpamEmail
from applications.authModel.models import Email

__author__ = 'AlexStarov'


class Command(BaseCommand, ):
    from optparse import make_option
    option_list = BaseCommand.option_list + (
        make_option('--id', '--pk', '--delivery_id', '--delivery_pk',
                    action='store', type='int', dest='delivery_pk',
                    help=''),
        make_option('--t', '--delivery_test', '--test',
                    action='store_true', dest='delivery_test',
                    help=''),
        make_option('--g', '--delivery_general', '--general',
                    action='store_true', dest='delivery_test',
                    help=''),
    )
    #self.verbosity = int(options.get('verbosity'))
    #def add_arguments(self, parser):
    #    parser.add_argument('delivery_id', nargs='+', type=int)

    def handle(self, *args, **options):
        cwd = os.getcwd()
        print(cwd, )
        cwd += '/applications/delivery/spam_txt_files'
        print(cwd, )
        dir = cwd
        bad_email = 0; good_email = 0; email_inserted = 0; email_exist_in_spam_list = 0; email_exist_in_emails = 0

        for name in os.listdir(dir):
            path_and_filename = os.path.join(dir, name)
            if os.path.isfile(path_and_filename, ):
                print('===============================================================================================================================', )
                print(path_and_filename, )
                f = open(name=path_and_filename, mode='r', buffering=True, )
                while True:
                    line = f.readline()
                    if not line: break
                    try:
                        email = line.split('<')[1].split('>')[0].lstrip('.')
                    except IndexError:
                        try:
                            email = line.strip()
                            validate_email(email, )
                        except ValidationError:
                            continue
                    print(line, email, ' bad_email: ', bad_email, ' good_email: ', good_email, )
                    """ Делаем повторную проверку на просто валидацию E-Mail адреса """
                    try:
                        EmailField().clean(email, )
                    except ValidationError:
                        bad_email += 1
                        email_error = u'Ваш E-Mail адрес не существует.'
                        print(email_error, )
                        continue
                    except DjangoUnicodeDecodeError:
                        bad_email += 1
                        email_error = u'Unicode Error.'
                        print(email_error, )
                        continue
                    else:
                        email_domain = email.split('@')[1]
                        if '.pn' in email_domain\
                                or '.jp' in email_domain\
                                or '.gi' in email_domain:
                            bad_email += 1
                            email_error = u'Ваш E-Mail адрес не существует.'
                            print(email_error, )
                            continue

                        good_email += 1
                        try:
                            SpamEmail.objects.get(email=email, )
                            email_exist_in_spam_list += 1
                            print('email_exist_in_spam_list: ', email_exist_in_spam_list, )
                            continue
                        except SpamEmail.DoesNotExist:
                            try:
                                Email.objects.get(email=email, )
                                email_exist_in_emails += 1
                                print('email_exist_in_emails: ', email_exist_in_emails, )
                                continue
                            except Email.DoesNotExist:
                                SpamEmail.objects.create(email=email, )
                                email_inserted += 1
                                print('email_inserted: ', email_inserted, )
                        except SpamEmail.MultipleObjectsReturned:
                            exist_emails = SpamEmail.objects.filter(email=email, )
                            exist_emails[0].delete()

                f.close()
            else:
                print('None', )
                # walk(path)
        print('email_inserted: ', email_inserted, )
        print('email_exist_in_emails: ', email_exist_in_emails, )
        print('email_exist_in_spam_list: ', email_exist_in_spam_list, )

def hernya3():
        from applications.delivery.models import Delivery
        try:
            deliveryes = Delivery.objects.filter(delivery_test=False, send_test=True, send_general=False, )
        except Delivery.DoesNotExist:
            deliveryes = None
        else:
            from applications.delivery.models import EmailMiddleDelivery
            for delivery in deliveryes:
                # print('delivery', delivery
                try:
                    EmailMiddleDelivery.objects.\
                        get(delivery=delivery,
                            send_test=False,
                            send_general=True,
                            updated_at__lte=delivery.updated_at, )
                except:
                    """ Создаем ссылочку на отсылку рассылки """
                    email_middle_delivery = EmailMiddleDelivery()
                    email_middle_delivery.delivery = delivery
                    email_middle_delivery.delivery_test_send = False
                    email_middle_delivery.delivery_send = True
                    email_middle_delivery.save()
                    """ Закрываем отсылку теста в самой рассылке """
                    delivery.send_general = True
                    delivery.save()
                    """ Отсылаем тестовое письмо """
                    from django.utils.html import strip_tags

                    EMAIL_USE_TLS = True
                    EMAIL_HOST = 'smtp.yandex.ru'
                    EMAIL_PORT = 587
                    EMAIL_HOST_USER = 'subscribe@keksik.com.ua'
                    EMAIL_HOST_PASSWORD = ''
                    from django.core.mail import get_connection
                    backend = get_connection(backend='django.core.mail.backends.smtp.EmailBackend',
                                             host=EMAIL_HOST,
                                             port=EMAIL_PORT,
                                             username=EMAIL_HOST_USER,
                                             password=EMAIL_HOST_PASSWORD,
                                             use_tls=EMAIL_USE_TLS,
                                             fail_silently=False, )
                    from django.core.mail import EmailMultiAlternatives
                    from proj.settings import Email_MANAGER

                    from applications.authModel.models import Email
                    """ Создаем указатели на E-Mail адреса рассылки """
                    try:
                        emails = Email.objects.filter(bad_email=False, )
                    except Email.DoesNotExist:
                        emails = None
                    """ Здесь нужно помудрить с коммитом """
                    from applications.delivery.models import EmailForDelivery
                    from applications.delivery.utils import parsing
                    i = 0
                    time = 0
                    for real_email in emails:
                        i += 1
                        # if i < 125:
                        #     continue
                        email = EmailForDelivery.objects.create(delivery=email_middle_delivery,
                                                                email=real_email, )
                        """ Отсылка """
                        msg = EmailMultiAlternatives(subject=delivery.subject,
                                                     body=strip_tags(parsing(value=delivery.html,
                                                                             key=email.key, ), ),
                                                     from_email='subscribe@keksik.com.ua',
                                                     to=[real_email.email, ],
                                                     connection=backend, )
                        msg.attach_alternative(content=parsing(value=delivery.html,
                                                               key=email.key, ),
                                               mimetype="text/html", )
                        msg.content_subtype = "html"
                        try:
                            msg.send(fail_silently=False, )
                        except Exception as e:
                            msg = EmailMultiAlternatives(subject='Error for subject: %s' % delivery.subject,
                                                         body='Error: %s - E-Mail: %s - real_email.pk: %d' % (e, real_email.email, real_email.pk, ),
                                                         from_email='subscribe@keksik.com.ua',
                                                         to=['subscribe@keksik.com.ua', ],
                                                         connection=backend, )
                            msg.send(fail_silently=True, )
                        else:
                            print('i: ', i, 'Pk: ', real_email.pk, ' - ', real_email.email
                            from random import randrange
                            time1 = randrange(6, 12, )
                            time2 = randrange(6, 12, )
                            time += time1 + time2
                            print('Time1: ', time1, ' Time2: ', time2, ' Time all: ', time1+time2, ' average time: ', time/i
                            from time import sleep
                            sleep(time1, )
                            print('Next'
                            sleep(time2, )



def hernya2():
        try:
            deliveryes = Delivery.objects.filter(delivery_test=False, )
        except Delivery.DoesNotExist:
            deliveryes = None
        else:
            for delivery in deliveryes:
                try:

                    aaa=EmailMiddleDelivery.objects.\
                        get(delivery=delivery, updated_at__lte=delivery.updated_at, )
                    print(aaa, delivery.updated_at
                except:
                    email_middle_delivery = EmailMiddleDelivery()
                    email_middle_delivery.delivery = delivery
                    email_middle_delivery.delivery_test_send = False
                    email_middle_delivery.delivery_send = True
                    email_middle_delivery.save()
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
                    print(real_email.email
                        #try:
                        #    # msg.send(fail_silently=False, )
                        #except Exception as inst:
                        #    print(type(inst, )
                        #    print(inst.args
                        #    print(inst
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
    print(datetime.now()
    from applications.product.models import Category
    try:
        action_category = Category.objects.get(url=u'акции', )
    except Category.DoesNotExist:
        action_category = None
    from applications.discount.models import Action
    action_active = Action.objects.active()
    if action_active:
        print('Action - ACTIVE:', action_active
        for action in action_active:
            products_of_action = action.product_in_action.all()
            print('All products:', products_of_action
            # print(action
            """
                Если акция с автостартом,
                то мы еЁ стартуем.
            """
            if action.auto_start:
                """ Включаем галочку 'Учавствует в акции' всем продуктам которые внесены в акцию
                    исключая продукты 'отсутсвующие на складе' """
                products_of_action = action.product_in_action.exclude(is_availability=4, )
                if len(products_of_action, ) > 0:
                    print('Product auto_start:', products_of_action
                    for product in products_of_action:
                        """ Помечает товар как учавствующий в акции """
                        product.in_action = True
                        """ Добавляем категорию 'Акция' в товар """
                        product.category.add(action_category, )
                        product.save()
                """ Удаляем товары учавствующие в активной акции но при этом 'отсутсвующие на складе' """
                products_remove_from_action = action.product_in_action.exclude(is_availability__lt=4, )
                if len(products_of_action, ) > 0:
                    print('Product auto_start:', products_of_action, )
                    for product in products_remove_from_action:
                        """ Помечает товар как учавствующий в акции """
                        product.in_action = False
                        """ Добавляем категорию 'Акция' в товар """
                        product.category.remove(action_category, )
                        product.save()
    action_not_active = Action.objects.not_active()
    if action_not_active:
        print('Action - NOT ACTIVE:', action_not_active, )
        for action in action_not_active:
            products_of_action = action.product_in_action.all()
            print('All products:', products_of_action, )
            # print(action
            """
                Если акция с авто окончанием,
                то заканчиваем еЁ.
            """
            if action.auto_end:
                products_of_action = action.product_in_action.in_action()
                if len(products_of_action, ) > 0:
                    print('Product auto_end:', products_of_action
                    for product in products_of_action:
                        print('Del product from Action: ', product
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
    from applications.product.models import Product
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
