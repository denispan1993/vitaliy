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

#                    from apps.delivery.models import MailAccount
#                    mail_accounts = MailAccount.objects.filter(is_active=True, ).order_by('?')
#                    len_mail_accounts = len(mail_accounts, )
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
                        for real_email_spam, real_email_try in emails_spam, emails_try:

                            print real_email_spam.content_type.model_class(), ': ', real_email_spam.email.email, real_email_try.content_type.model_class(), ': ', real_email_try.email.email

