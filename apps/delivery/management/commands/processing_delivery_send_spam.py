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

                    from apps.authModel.models import Email
                    count_emails_try = Email.objects.filter(bad_email=False, ).count()

                    import sys

                    from apps.delivery.models import EmailForDelivery
                    from apps.delivery.utils import parsing
                    from django.utils.html import strip_tags
                    from time import sleep
                    from django.core.mail import EmailMultiAlternatives
                    from apps.delivery.utils import Mail_Account, Backend, Test_Server_MX_from_email, get_email,\
                        create_msg, connect, send_msg, sleep_now
                    i = 0
                    time = 0
                    import dns.resolver
                    resolver = dns.resolver.Resolver()
                    resolver.nameservers = ['192.168.1.100', ]
                    from apps.authModel.models import Email
                    from apps.delivery.models import SpamEmail
                    for n in range(1, count_emails_try, ):
                        mail_account = Mail_Account()
                        email = get_email(delivery=delivery, email_class=Email, )
                        print 'n: ', n, 'in: ', count_emails_try
                        if email:
                            if not Test_Server_MX_from_email(email_string=email.email, resolver=resolver, ):
                                email.bad_email = True
                                email.save()
                            else:
                                i += 1
                                email = EmailForDelivery.objects.create(delivery=email_middle_delivery,
                                                                        # content_type=real_email.content_type,
                                                                        # object_id=real_email.pk,
                                                                        now_email=email, )
                                """ Отсылка """
                                from apps.delivery.utils import create_msg, connect, send_msg
                                msg = create_msg(delivery=delivery, mail_account=mail_account, email=email, test=False, )
                                from smtplib import SMTPSenderRefused, SMTPDataError
                                connection = connect(mail_account=mail_account, fail_silently=False, )
                                try:
                                    send_msg(connection=connection, mail_account=mail_account, email=email, msg=msg, )
                                except SMTPSenderRefused as e:
                                    print 'SMTPSenderRefused: ', e
                                    email.delete()
                                    sleep(30, )
                                    time += 30
                                except SMTPDataError as e:
                                    print 'SMTPDataError: ', e
                                    print 'SMTPDataError: smtp_code', e.smtp_code
                                    print 'SMTPDataError: smtp_error', e.smtp_error
                                    print 'SMTPDataError: args', e.args
                                    print 'SMTPDataError: message', e.message
                                    if e.smtp_code == 554 and "5.7.1 Message rejected under suspicion of SPAM;" in e.smtp_error:
                                        print 'SPAM Bloked E-Mail: ', mail_account, ' NOW !!!!!!!!!!!!!!!!!!!!!!!'
                                        from datetime import datetime
                                        mail_account.is_auto_active = False
                                        mail_account.auto_active_datetime = datetime.now()
                                        mail_account.save()
                                    connection = connect(mail_account=mail_account, fail_silently=True, )
                                    msg = create_msg(delivery=delivery, mail_account=mail_account, email=email, exception=e, test=False, )
                                    send_msg(connection=connection, mail_account=mail_account, email=email, msg=msg, execption=e, )
                                    email.delete()
                                    sleep(30, )
                                    time += 30
                                except Exception as e:
                                    print 'Exception: ', e
                                    email.delete()
                                time = sleep_now(time=time, email=email, i=i, )

#====================== SPAM
                        email = get_email(delivery=delivery, email_class=SpamEmail, )
                        if email:
                            if not Test_Server_MX_from_email(email_string=email.email, resolver=resolver, ):
                                email.bad_email = True
                                email.save()
                            else:
                                i += 1
                                email = EmailForDelivery.objects.create(delivery=email_middle_delivery,
                                                                        # content_type=real_email.content_type,
                                                                        # object_id=real_email.pk,
                                                                        now_email=email, )
                                """ Отсылка """
                                from apps.delivery.utils import create_msg, connect, send_msg
                                msg = create_msg(delivery=delivery, mail_account=mail_account, email=email, test=False, )
                                from smtplib import SMTPSenderRefused, SMTPDataError
                                connection = connect(mail_account=mail_account, fail_silently=False, )
                                try:
                                    send_msg(connection=connection, mail_account=mail_account, email=email, msg=msg, )
                                except SMTPSenderRefused as e:
                                    print 'SMTPSenderRefused: ', e
                                    email.delete()
                                    sleep(30, )
                                    time += 30
                                except SMTPDataError as e:
                                    print 'SMTPDataError: ', e
                                    if e.smtp_code == 554 and "5.7.1 Message rejected under suspicion of SPAM;" in e.smtp_error:
                                        print 'SPAM Bloked E-Mail: ', mail_account, ' NOW !!!!!!!!!!!!!!!!!!!!!!!'
                                        from datetime import datetime
                                        mail_account.is_auto_active = False
                                        mail_account.auto_active_datetime = datetime.now()
                                        mail_account.save()
                                    connection = connect(mail_account=mail_account, fail_silently=True, )
                                    msg = create_msg(delivery=delivery, mail_account=mail_account, email=email, exception=e, test=False, )
                                    send_msg(connection=connection, mail_account=mail_account, email=email, msg=msg, execption=e, )
                                    email.delete()
                                    sleep(30, )
                                    time += 30
                                except Exception as e:
                                    print 'Exception: ', e
                                    email.delete()
                                time = sleep_now(time=time, email=email, i=i, )
