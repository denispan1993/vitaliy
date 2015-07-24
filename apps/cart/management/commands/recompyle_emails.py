# coding=utf-8
__author__ = 'user'

from django.core.management.base import BaseCommand

from pytils.translit import slugify


class Command(BaseCommand, ):
    def handle(self, *args, **options):
        from apps.authModel.models import Email

        emails = Email.objects.all()
        i = 0; n = 1
        email_content = ''
        for email in emails:
            if i > 10:
                from django.core.mail import get_connection
                backend = get_connection(backend='django.core.mail.backends.smtp.EmailBackend',
                                         fail_silently=False, )
                from django.core.mail import EmailMultiAlternatives
                msg = EmailMultiAlternatives(subject="Email's № %d" % n,
                                             body=email_content,
                                             from_email=u'site@keksik.com.ua',
                                             to=[u'lana24680@keksik.com.ua', ],
                                             connection=backend, )
                msg.content_subtype = "html"
                msg.send(fail_silently=False, )
                n += 1
                email_content = ''
                i = 0
                print n
                print email_content
            else:
                i += 1
                print i

            email_content += '%s, ' % email.email
