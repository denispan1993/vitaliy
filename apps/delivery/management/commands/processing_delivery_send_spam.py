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
                    from time import sleep
                    from random import randrange
                    from django.utils.html import strip_tags

                    from django.core.mail import EmailMultiAlternatives
                    from apps.delivery.utils import Mail_Account, Backend, Test_Server_MX_from_email, get_email
                    i = 0
                    time = 0
                    import dns.resolver
                    resolver = dns.resolver.Resolver()
                    resolver.nameservers = ['192.168.1.100', ]
                    from apps.authModel.models import Email
                    from apps.delivery.models import SpamEmail
                    for n in range(1, count_emails_try, ):
                        mail_account = Mail_Account()
                        backend = Backend(mail_account=mail_account, )
                        email = get_email(delivery=delivery, email_class=Email, )
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
                            msg = EmailMultiAlternatives(subject=delivery.subject,
                                                         body=strip_tags(parsing(value=delivery.html,
                                                                                 key=email.key, ), ),
                                                         from_email=u'Интернет магазин Кексик <%s>' % mail_account.email,
                                                         to=[email.now_email.email, ],
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
                            except smtplib.SMTPDataError as e:
                                print e
                                email.delete()
                                print 'SMTPDataError'
                                sleep(30, )
                                time += 30
                            except Exception as e:
                                print e
                                msg = EmailMultiAlternatives(subject='Error for subject: %s' % delivery.subject,
                                                             body='Error: %s - E-Mail: %s - real_email.pk: %d' % (e, email.now_email.email, email.now_email.pk, ),
                                                             from_email=u'Интернет магазин Кексик <%s>' % mail_account.email,
                                                             to=[mail_account.email, ],
                                                             connection=backend, )
                                print '7'
                                msg.send(fail_silently=True, )
                                sleep(5, ); print 'sleep1, '; sleep(5, ); print 'sleep2, '; sleep(5, ); print 'sleep3'
                                time += 15
                                print '8'
                            else:
                                print 'i: ', i, 'Pk: ', email.now_email.pk, ' - ', email.now_email.email
                                time1 = randrange(7, 19, )
                                time2 = randrange(7, 19, )
                                time += time1 + time2
                                print 'Time1: ', time1, ' Time2: ', time2, ' Time all: ', time1+time2, ' average time: ', time/i
                                for n in range(1, time1, ):
                                    print '.',
                                    sys.stdout.flush()
                                    sleep(1, )
                                print '\n'
                                for n in range(1, time2, ):
                                    print '.',
                                    sys.stdout.flush()
                                    sleep(1, )
                                print '\n'
#====================== SPAM
                        mail_account = Mail_Account()
                        backend = Backend(mail_account=mail_account, )
                        email = get_email(delivery=delivery, email_class=SpamEmail, )
                        if not Test_Server_MX_from_email(email_string=email.email, resolver=resolver, ):
                            email.bad_email = True
                            email.save()
                        else:
                            i += 1
                            email = EmailForDelivery.objects.create(delivery=email_middle_delivery,
                                                                    now_email=email, )
                            """ Отсылка """
                            msg = EmailMultiAlternatives(subject=delivery.subject,
                                                         body=strip_tags(parsing(value=delivery.html,
                                                                                 key=email.key, ), ),
                                                         from_email=u'Интернет магазин Кексик <%s>' % mail_account.email,
                                                         to=[email.now_email.email, ],
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
                            except smtplib.SMTPDataError as e:
                                print e
                                email.delete()
                                print 'SMTPDataError'
                                sleep(30, )
                                time += 30
                            except Exception as e:
                                print e
                                msg = EmailMultiAlternatives(subject='Error for subject: %s' % delivery.subject,
                                                             body='Error: %s - E-Mail: %s - real_email.pk: %d' % (e, email.now_email.email, email.now_email.pk, ),
                                                             from_email=u'Интернет магазин Кексик <%s>' % mail_account.email,
                                                             to=[mail_account.email, ],
                                                             connection=backend, )
                                print '7'
                                msg.send(fail_silently=True, )
                                sleep(5, ); print 'sleep1, '; sleep(5, ); print 'sleep2, '; sleep(5, ); print 'sleep3'
                                time += 15
                                print '8'
                            else:
                                print 'i: ', i, 'Pk: ', email.now_email.pk, ' - ', email.now_email.email
                                time1 = randrange(7, 19, )
                                time2 = randrange(7, 19, )
                                time += time1 + time2
                                print 'Time1: ', time1, ' Time2: ', time2, ' Time all: ', time1+time2, ' average time: ', time/i
                                for n in range(1, time1, ):
                                    print '.',
                                    sys.stdout.flush()
                                    sleep(1, )
                                print '\n'
                                for n in range(1, time2, ):
                                    print '.',
                                    sys.stdout.flush()
                                    sleep(1, )
                                print '\n'
