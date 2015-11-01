# -*- coding: utf-8 -*-
__author__ = 'AlexStarov'

from django.core.management.base import BaseCommand


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
        from apps.delivery.models import Delivery
        try:
            deliveryes = Delivery.objects.filter(delivery_test=False,
                                                 send_test=True, send_spam=False, send_general=False,
                                                 type__in=[4, ], )
            #deliveryes = Delivery.objects.all()
            #for delivery in deliveryes:
            #    print delivery.delivery_test
            #    print delivery.send_test
            #    print delivery.send_spam
            #    print delivery.send_general
            #    print delivery.type
        except Delivery.DoesNotExist:
            deliveryes = None
        else:
            from apps.delivery.models import EmailMiddleDelivery
            for delivery in deliveryes:
                print delivery
                # print 'delivery', delivery
                try:
                    EmailMiddleDelivery.objects.\
                        get(delivery=delivery,
                            delivery_test_send=False,
                            spam_send=True,
                            delivery_send=False,
                            updated_at__gte=delivery.updated_at, )
                except:
                    """ Создаем ссылочку на отсылку рассылки """
                    email_middle_delivery = EmailMiddleDelivery()
                    email_middle_delivery.delivery = delivery
                    email_middle_delivery.delivery_test_send = False
                    email_middle_delivery.spam_send = True
                    email_middle_delivery.delivery_send = False
                    email_middle_delivery.save()
                    """ Закрываем отсылку теста в самой рассылке """
                    delivery.send_spam = True
                    delivery.save()
                    print delivery
                    """ Отсылаем тестовое письмо """
                    from django.utils.html import strip_tags

                    from apps.delivery.models import MailAccount
                    mail_accounts = MailAccount.objects.filter(is_active=True, ).order_by('?')
                    last_mail_accounts = MailAccount.objects.latest('pk', )
                    len_mail_accounts = len(mail_accounts, )
                    EMAIL_USE_TLS = False
                    EMAIL_USE_SSL = True
                    #EMAIL_HOST = 'smtp.yandex.ru'
#                    EMAIL_HOST = 'smtp.rambler.ru'
                    EMAIL_HOST = 'smtp.mail.ru'
                    #EMAIL_PORT = 587
                    EMAIL_PORT = 465
                    #EMAIL_PORT = 2525
                    #EMAIL_HOST_USER = 'webwww@keksik.com.ua'
#                    EMAIL_HOST_USER = 'subscribe.keksik.com@rambler.ru'
                    EMAIL_HOST_USER = 'subscribe.keksik@mail.ru'
                    SERVER_EMAIL = 'subscribe.keksik@mail.ru'
                    #EMAIL_HOST_PASSORD = '1q2w3e4r'
                    EMAIL_HOST_PASSORD = '1q2w3e4r21'
                    from django.core.mail import get_connection
                    backend = get_connection(backend='django.core.mail.backends.smtp.EmailBackend',
                                             host=EMAIL_HOST,
                                             port=EMAIL_PORT,
                                             username=EMAIL_HOST_USER,
                                             passord=EMAIL_HOST_PASSORD,
                                             use_tls=EMAIL_USE_TLS,
                                             fail_silently=False,
                                             use_ssl=EMAIL_USE_SSL,
                                             timeout=10, )
                    from django.core.mail import EmailMultiAlternatives
                    from proj.settings import Email_MANAGER

                    from apps.authModel.models import Email
                    """ Создаем указатели на E-Mail адреса рассылки """
                    try:
                        emails_try = Email.objects.filter(bad_email=False, ).order_by('?')
                    except Email.DoesNotExist:
                        emails_try = None

                    from apps.delivery.models import SpamEmail
                    """ Создаем указатели на E-Mail адреса рассылки """
                    try:
                        emails_spam = SpamEmail.objects.filter(bad_email=False, ).order_by('?')
                    except SpamEmail.DoesNotExist:
                        emails_spam = None
                    else:
                        from apps.delivery.models import EmailForDelivery
                        from apps.delivery.utils import parsing
                        from time import sleep
                        from random import randrange
                        i = 0
                        time = 0
                        # for real_email in emails:
                        for real_email_try in emails_try:
                            try:
                                print real_email_try
                                print real_email_try.content_type
                                print real_email_try.content_type.model_class()
                                print real_email_try.content_type.natural_key()
                                from django.contrib.contenttypes.models import ContentType

                                email = EmailForDelivery.objects.get(content_type=real_email_try.content_type,
                                                                     object_id=real_email_try.pk, )
                            except EmailForDelivery.DoesNotExist:
                                pass
                            except EmailForDelivery.MultipleObjectsReturned:
                                emails = EmailForDelivery.objects.filter(content_type=real_email_try.content_type,
                                                                         object_id=real_email_try.pk, )
                                emails[0].delete()
                            else:
                                print 'Exist: ', email.now_email.email
                                continue
                            i += 1
                            loop = True
                            while loop:
                                mail_account_pk = randrange(1, last_mail_accounts.pk, )
                                try:
                                    mail_account = mail_accounts.get(pk=mail_account_pk, )
                                except MailAccount.DoesNotExist:
                                    print 'No: ', mail_account_pk
                                else:
                                    print 'Yes:', mail_account_pk; loop = False
                            print mail_account
                            backend = get_connection(backend='django.core.mail.backends.smtp.EmailBackend',
                                                     host=mail_account.server.server,
                                                     port=mail_account.server.port,
                                                     username=mail_account.username,
                                                     password=mail_account.password,
                                                     use_tls=mail_account.server.use_tls,
                                                     fail_silently=False,
                                                     use_ssl=mail_account.server.use_ssl, )
                            # if i < 125:
                            #     continue
                            #email = EmailForDelivery.objects.create(delivery=email_middle_delivery,
                            #                                        content_type=real_email.content_type,
                            #                                        object_id=real_email.pk, )
                            #                                        # now_email=real_email, )
                            email = EmailForDelivery.objects.create(delivery=email_middle_delivery,
                                                                    # content_type=real_email.content_type,
                                                                    # object_id=real_email.pk,
                                                                    now_email=real_email_try, )
                            """ Отсылка """
                            msg = EmailMultiAlternatives(subject=delivery.subject,
                                                         body=strip_tags(parsing(value=delivery.html,
                                                                                 key=email.key, ), ),
                                                         from_email=u'Интернет магазин Кексик <%s>' % mail_account.email,
#                                                         from_email=u'Интернет магазин Кексик <webwww@keksik.com.ua>',
#                                                         from_email=u'Интернет магазин Кексик <subscribe.keksik.com@rambler.ru>',
#                                                         from_email=u'Интернет магазин Кексик <subscribe.keksik@mail.ru>',
                                                         to=[real_email_try.email, ],
                                                         connection=backend, )
                            msg.attach_alternative(content=parsing(value=delivery.html,
                                                                   key=email.key, ),
                                                   mimetype="text/html", )
                            msg.content_subtype = "html"
                            import smtplib
                            try:
                                msg.send(fail_silently=False, )
                            except smtplib.SMTPSenderRefused as e:
                                print e
                                email.delete()
                                print 'SMTPSenderRefused'
                                sleep(30, )
                                time += 30
                            except Exception as e:
#                                print mail_account.email
                                print e
                                msg = EmailMultiAlternatives(subject='Error for subject: %s' % delivery.subject,
                                                             body='Error: %s - E-Mail: %s - real_email.pk: %d' % (e, real_email_try.email, real_email_try.pk, ),
                                                             from_email=u'Интернет магазин Кексик <%s>' % mail_account.email,
#                                                             from_email=mail_account.email,
#                                                             from_email='webwww@keksik.com.ua',
#                                                             from_email='subscribe.keksik.com@rambler.ru',
#                                                             from_email='subscribe.keksik@mail.ru',
                                                             to=[mail_account.email, ],
#                                                             to=['webwww@keksik.com.ua', ],
#                                                             to=['subscribe.keksik.com@rambler.ru', ],
#                                                             to=['subscribe.keksik@mail.ru', ],
                                                             connection=backend, )
                                print '7'
                                msg.send(fail_silently=True, )
                                sleep(5, ); print 'sleep1, '; sleep(5, ); print 'sleep2, '; sleep(5, ); print 'sleep3'
                                time += 15
                                print '8'
                            else:
                                print 'i: ', i, 'Pk: ', real_email_try.pk, ' - ', real_email_try.email
                                time1 = randrange(10, 20, )
                                time2 = randrange(10, 20, )
                                time += time1 + time2
                                print 'Time1: ', time1, ' Time2: ', time2, ' Time all: ', time1+time2, ' average time: ', time/i
                                for n in range(1, time1, ):
                                    print '.',
                                    sleep(1, )
                                print 'Next'
                                for n in range(1, time2, ):
                                    print '.',
                                    sleep(1, )
                            try:
                                try:
                                    print emails_spam[real_email_try.pk]
                                    print emails_spam[real_email_try.pk].content_type
                                    print emails_spam[real_email_try.pk].content_type.model_class()
                                    print emails_spam[real_email_try.pk].content_type.natural_key()
                                    from django.contrib.contenttypes.models import ContentType

                                    email = EmailForDelivery.objects.get(content_type=emails_spam[real_email_try.pk].content_type,
                                                                         object_id=emails_spam[real_email_try.pk].pk, )
                                except IndexError:
                                    continue
                            except EmailForDelivery.DoesNotExist:
                                pass
                            except EmailForDelivery.MultipleObjectsReturned:
                                emails = EmailForDelivery.objects.filter(content_type=emails_spam[real_email_try.pk].content_type,
                                                                         object_id=emails_spam[real_email_try.pk].pk, )
                                emails[0].delete()
                            else:
                                print 'Exist: ', email.now_email.email
                                continue
                            email = EmailForDelivery.objects.create(delivery=email_middle_delivery,
                                                                    # content_type=real_email.content_type,
                                                                    # object_id=real_email.pk,
                                                                    now_email=emails_spam[real_email_try.pk], )
                            """ Отсылка """
                            print mail_account
                            msg = EmailMultiAlternatives(subject=delivery.subject,
                                                         body=strip_tags(parsing(value=delivery.html,
                                                                                 key=email.key, ), ),
                                                         from_email=u'Интернет магазин Кексик <%s>' % mail_account.email,
                                                         to=[emails_spam[real_email_try.pk].email, ],
                                                         connection=backend, )
                            msg.attach_alternative(content=parsing(value=delivery.html,
                                                                   key=email.key, ),
                                                   mimetype="text/html", )
                            msg.content_subtype = "html"
                            import smtplib
                            try:
                                msg.send(fail_silently=False, )
                            except smtplib.SMTPSenderRefused as e:
                                print e
                                email.delete()
                                print 'SMTPSenderRefused'
                                sleep(30, )
                                time += 30
                            except Exception as e:
#                                print mail_account.email
                                print e
                                msg = EmailMultiAlternatives(subject='Error for subject: %s' % delivery.subject,
                                                             body='Error: %s - E-Mail: %s - real_email.pk: %d' % (e, emails_spam[real_email_try.pk].email, emails_spam[real_email_try.pk].pk, ),
                                                             from_email=u'Интернет магазин Кексик <%s>' % mail_account.email,
                                                             to=[mail_account.email, ],
                                                             connection=backend, )
                                print '7'
                                msg.send(fail_silently=True, )
                                sleep(5, ); print 'sleep1, '; sleep(5, ); print 'sleep2, '; sleep(5, ); print 'sleep3'
                                time += 15
                                print '8'
                            else:
                                print 'i: ', i, 'Pk: ', emails_spam[real_email_try.pk].pk, ' - ', emails_spam[real_email_try.pk].email
                                time1 = randrange(10, 20, )
                                time2 = randrange(10, 20, )
                                time += time1 + time2
                                print 'Time1: ', time1, ' Time2: ', time2, ' Time all: ', time1+time2, ' average time: ', time/i
                                for n in range(1, time1, ):
                                    print '.',
                                    sleep(1, )
                                print 'Next'
                                for n in range(1, time2, ):
                                    print '.',
                                    sleep(1, )



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
                    print aaa, delivery.updated_at
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
    print datetime.no()
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
