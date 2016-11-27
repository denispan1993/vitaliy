# -*- coding: utf-8 -*-
# /apps/delivery2/models.py

import os
import hashlib
import re
from random import randint
import time
from datetime import datetime, timedelta
from celery.result import AsyncResult
from celery.utils import uuid

from django.db import models, IntegrityError
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_unicode
from django.utils.baseconv import base62
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.template.loader import render_to_string
from django.db.models import Q

import proj.settings
from compat.ImageWithThumbs import models as class_ImageWithThumb
from apps.utils.captcha.views import key_generator
from apps.cart.models import Order
from apps.authModel.models import Email as authModel_Email
from apps.delivery.models import SpamEmail as delivery_Email

__author__ = 'AlexStarov'

EMAIL_UNSUBSCRIBE_LINK = 'http://{host}/email/unsubscribe?code={code}'

TAG_REPLACE = {
    '#UNSUBSCRIBE_URL#': EMAIL_UNSUBSCRIBE_LINK\
        .format(host=proj.settings.SENDER_DOMAIN, code='{{ email_hash }}'),
    # '#SHOW_ONLINE_URL#':,
    # '#OPEN_URL#':,
    # '#GOOGLE_URL#':,
}


def upload_to(instance, filename, prefix=None, unique=True):
    """
    Auto generate name for File and Image fields.
    :param instance: Instance of Model
    :param filename: Name of uploaded file
    :param prefix: Add to filename
    :param unique: Unique for the same instance and filename
    :return:
    """
    ext = os.path.splitext(filename)[1]
    name = str(instance.pk or '') + filename + (str(time.time()) if unique else '')

    # We think that we use utf8 based OS file system
    filename = hashlib.md5(name.encode('utf8')).hexdigest() + ext
    basedir = os.path.join(instance._meta.app_label, instance.__class__.__name__)
    if prefix:
        basedir = os.path.join(basedir, prefix)
    return os.path.join(basedir, filename[:2], filename[2:4], filename)


def datetime_in_iso_format():
    return datetime.now().isoformat()


class Delivery(models.Model, ):
    name = models.CharField(verbose_name=_(u'Имя рассылки', ),
                            max_length=128,
                            blank=True,
                            null=True,
                            default=datetime_in_iso_format, )

    can_send = models.BooleanField(verbose_name=_(u'Разрешено отправлять рассылку', ),
                                   blank=True,
                                   null=False,
                                   default=False, )

    is_active = models.BooleanField(verbose_name=_(u'Рассылка идет', ),
                                    blank=True,
                                    null=False,
                                    default=False, )
    task_id = models.CharField(verbose_name=_(u'task id'),
                               max_length=255,
                               blank=True,
                               null=True, )
                               # editable=False)

    delivery_test = models.BooleanField(verbose_name=_(u'Тестовая рассылка', ),
                                        blank=True,
                                        null=False,
                                        default=True, )
    test_send = models.BooleanField(verbose_name=_(u'Тестовая рассылка отослана', ),
                                    blank=True,
                                    null=False,
                                    default=False, )
    general_send = models.BooleanField(verbose_name=_(u'Главная рассылка отослана', ),
                                       blank=True,
                                       null=False,
                                       default=False, )
    Type_Mailings = (
        (1, _(u'Системная', ), ),
        (2, _(u'Акция', ), ),
        (4, _(u'Новинки', ), ),
    )
    type = models.PositiveSmallIntegerField(verbose_name=_(u'Тип рассылки'),
                                            choices=Type_Mailings,
                                            default=1,
                                            blank=False,
                                            null=False, )

#    template = models.ForeignKey(to='EmailTemplate',
#                                 related_name='delivery_EmailTemplate',
#                                 verbose_name=_(u'Template', ),
#                                 blank=True,
#                                 null=True, )

    #Дата Рассылки.
    started_at = models.DateTimeField(verbose_name=_(u'Дата и время рассылки', ),
                                      blank=True,
                                      null=True, )

    #Дата создания и дата обновления. Устанавливаются автоматически.
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name=_(u'Дата создания', ),
                                      blank=True,
                                      null=True, )
    updated_at = models.DateTimeField(auto_now=True,
                                      verbose_name=_(u'Дата обновления', ),
                                      blank=True,
                                      null=True, )

    def schedule_run(self, ):
        from .tasks import send_delivery

        if self.task_id:
            AsyncResult(self.task_id).revoke()
        self.task_id = None
        started_at = self.started_at
        self.started_at = None
        task = send_delivery.apply_async(queue='celery',
                                         kwargs={'delivery_pk': self.pk},
                                         task_id='celery-task-id-{0}'.format(uuid(), ),
                                         eta=started_at)
        self.task_id = task.id
        print('Start Delivery at: ', started_at, self.started_at)

        self.save(skip_schedule=True, )

    def save(self, *args, **kwargs):

        if not kwargs.pop('skip_schedule', False)\
                and not self.task_id\
                and not self.is_active\
                and self.started_at\
                and self.started_at.replace(tzinfo=None) > datetime.now():
            print self.started_at.replace(tzinfo=None)
            print datetime.now()
            self.schedule_run()

        super(Delivery, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'Рассылка: № %6d: %s' % (self.pk, self.name, )

    class Meta:
        db_table = 'Delivery2_Delivery'
        ordering = ['-created_at', ]
        verbose_name = _(u'Рассылка', )
        verbose_name_plural = _(u'Рассылки', )


class EmailSubject(models.Model, ):
    """ subject будующей рассылки """
    delivery = models.ForeignKey(to=Delivery,
                                 related_name='subjects',
                                 blank=False,
                                 null=False,)

    subject = models.CharField(verbose_name=_(u'Тема письма', ),
                               max_length=256,
                               blank=False,
                               null=False,
                               default=datetime.now, )

    chance = models.DecimalField(verbose_name=_(u'Вероятность', ),
                                 max_digits=4,
                                 decimal_places=2,
                                 blank=False,
                                 null=False,
                                 default=1, )

    #Дата создания и дата обновления. Устанавливаются автоматически.
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name=_(u'Дата создания', ),
                                      blank=True,
                                      null=True, )
    updated_at = models.DateTimeField(auto_now=True,
                                      verbose_name=_(u'Дата обновления', ),
                                      blank=True,
                                      null=True, )

    def __unicode__(self):
        return u'Тема: № %6d: [%s]:%2.2f' % (self.pk, self.subject, self.chance )

    class Meta:
        db_table = 'Delivery2_EmailSubject'
        ordering = ['-created_at', ]
        verbose_name = _(u'Тема', )
        verbose_name_plural = _(u'Темы', )


class EmailTemplate(models.Model, ):
    """ template будующей рассылки """
    delivery = models.ForeignKey(to=Delivery,
                                 related_name='templates',
                                 blank=False,
                                 null=False, )

    name = models.CharField(max_length=64,
                            unique=True,
                            verbose_name=_(u'Название', ),
                            blank=True,
                            null=True,
                            default=datetime.now, )

    template = models.FileField(upload_to=upload_to,
                                verbose_name=_(u'Шаблон', ),
                                blank=True,
                                null=True, )

    chance = models.DecimalField(verbose_name=_(u'Вероятность', ),
                                 max_digits=4,
                                 decimal_places=2,
                                 blank=False,
                                 null=False,
                                 default=1, )

    #Дата создания и дата обновления. Устанавливаются автоматически.
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name=_(u'Дата создания', ),
                                      blank=True,
                                      null=True, )
    updated_at = models.DateTimeField(auto_now=True,
                                      verbose_name=_(u'Дата обновления', ),
                                      blank=True,
                                      null=True, )

    def get_image_and_style_names(self):
        self.template.file.seek(0)
        html = self.template.file.read()
        img = re.findall(r'url\([\'|\"](?P<file>[^ \s]+)[\'|\"]\)', html)
        style = re.findall(r'src=[\'|\"](?P<file>[^ \s]+)[\'|\"]', html)
        return set(img + style)

    def get_urls(self):
        self.template.file.seek(0)
        html = self.template.file.read()
        url = re.findall(r'<a\s+(?:[^>]*?\s+)?href="([^"]*)"', html)
        return set(url)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(EmailTemplate, self).save(force_insert, force_update, using, update_fields)
        images = self.get_image_and_style_names()

        for url in images:
            if not self.images.filter(url=url, ).exists():
                self.images.create(url=url, )

        urls = self.get_urls()

        for href in urls:
            if not self.urls.filter(href=href, ).exists():
                self.urls.create(href=href, )

        self.template.file.seek(0)
        html = self.template.file.read()

        for href in urls:
            href_pk = EmailUrlTemplate.objects\
                .values_list('id', flat=True)\
                .get(template_id=self.id,
                     href=href, )
            html = html.replace(href,
                                '#URL_{href_pk:06d}#'.format(href_pk=href_pk, ))

        with open(self.template.path, 'w') as f:
            f.write(html, )

    def get_template(self):
        self.template.file.seek(0)
        html = self.template.file.read()
        html = force_unicode(html)
        for image in self.images.all():
            if image.image.name:
                try:
                    html = html.replace(image.url,
                                        'http://{host}{url}'.format(host=proj.settings.IMAGE_STORE_HOST,
                                                                    url=image.image.url, ), )
                except Exception, e:
                    pass
        # TODO: Доделать ТЭГИ
        #for tag in TAG_REPLACE:
        #    html = html.replace(tag, TAG_REPLACE[tag])
        #html = RE_REPLACE_GENDER.sub(replace_gender_callback, html)
        #html = html.replace(
        #    '</body>',
        #    '<img src="http://{{ MAIN_DOMAIN }}{{ mail_obj.get_pixel_url }}" width="0" height="0" border="0" /></body>', )
        return html

    def __unicode__(self):
        if self.pk:
            return u'Тело письма: № %6d: %2.2f' % (self.pk, self.chance, )
        else:
            return u'Тело письма: № None: %2.2f' % self.chance

    class Meta:
        db_table = 'Delivery2_EmailTemplate'
        ordering = ['-created_at', ]
        verbose_name = _(u'Template письма', )
        verbose_name_plural = _(u'Templates писем', )


class EmailImageTemplate(models.Model, ):
    """ img in template будующей рассылки """
    template = models.ForeignKey(to=EmailTemplate,
                                 related_name='images',
                                 verbose_name=u'Шаблон',
                                 blank=False,
                                 null=False, )
    url = models.CharField(max_length=256, verbose_name=u'Путь')

    image = models.ImageField(upload_to=upload_to,
                              verbose_name=_(u'Изображение', ),
                              blank=True,
                              null=True, )

    #Дата создания и дата обновления. Устанавливаются автоматически.
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name=_(u'Дата создания', ),
                                      blank=True,
                                      null=True, )
    updated_at = models.DateTimeField(auto_now=True,
                                      verbose_name=_(u'Дата обновления', ),
                                      blank=True,
                                      null=True, )

    class Meta:
        db_table = 'Delivery2_EmailImageTemplate'
        ordering = ['-created_at', ]
        verbose_name = _(u'Изображение в письме', )
        verbose_name_plural = _(u'Изображения в письме', )


class EmailUrlTemplate(models.Model, ):
    """ url in template будующей рассылки """
    template = models.ForeignKey(to=EmailTemplate,
                                 related_name='urls',
                                 verbose_name=u'Шаблон',
                                 blank=False,
                                 null=False, )
    href = models.CharField(verbose_name=_(u'URL', ),
                            max_length=256,
                            blank=True,
                            null=True, )

    #Дата создания и дата обновления. Устанавливаются автоматически.
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name=_(u'Дата создания', ),
                                      blank=True,
                                      null=True, )
    updated_at = models.DateTimeField(auto_now=True,
                                      verbose_name=_(u'Дата обновления', ),
                                      blank=True,
                                      null=True, )

    def __unicode__(self):
        return u'pk:%0.6d [unsub] --> %s' % (
            self.pk,
            self.href, )

    class Meta:
        db_table = 'Delivery2_EmailUrlTemplate'
        ordering = ['-created_at', ]
        verbose_name = _(u'Url в темплэйте', )
        verbose_name_plural = _(u'Urls в темплэйте', )


class MessageRedirectUrl(models.Model, ):
    """ Связка URL в письме и куда будет редирект """
    id = models.BigIntegerField(primary_key=True, )

    delivery = models.ForeignKey(to=Delivery,
                                 verbose_name=_(u'Рассылка'),
                                 blank=False,
                                 null=False, )

    href = models.ForeignKey(to=EmailUrlTemplate,
                             verbose_name=_(u'Url', ),
                             blank=True,
                             null=True, )

    #Дата создания и дата обновления. Устанавливаются автоматически.
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name=_(u'Дата создания', ),
                                      blank=True,
                                      null=True, )
    updated_at = models.DateTimeField(auto_now=True,
                                      verbose_name=_(u'Дата обновления', ),
                                      blank=True,
                                      null=True, )

    @classmethod
    def code2int(cls, id_62, ):
        try:
            return base62.decode(id_62, )
        except Exception:
            raise ValueError

    def save(self, *args, **kwargs):
        while True:
            if not self.pk:
                self.pk = randint(1, 9223372036854775807)
            try:
                super(MessageRedirectUrl, self).save(*args, **kwargs)
            except IntegrityError:
                self.pk = None
            else:
                break

    @models.permalink
    def get_absolute_url(self):
        return 'email:go', [base62.encode(self.pk), ]

    def __unicode__(self):
        return u'pk:%0.6d [href:%s]' % (self.pk, self.href, )

    class Meta:
        db_table = 'Delivery2_MessageRedirectUrl'
        ordering = ['-created_at', ]
        verbose_name = _(u'Url', )
        verbose_name_plural = _(u'Urls', )


class Message(models.Model):
    delivery = models.ForeignKey(to=Delivery,
                                 verbose_name=_(u'Указатель на рассылку', ),
                                 blank=False,
                                 null=False, )

    is_send = models.BooleanField(verbose_name=_(u'Рассылка отослана', ),
                                  blank=True,
                                  null=False,
                                  default=False, )

    content_type = models.ForeignKey(ContentType,
                                     related_name='delivery_Message',
                                     verbose_name=_(u'Указатель на E-Mail', ),
                                     blank=True,
                                     null=True, )
    object_id = models.PositiveIntegerField(db_index=True,
                                            blank=True,
                                            null=True, )
    email = GenericForeignKey('content_type', 'object_id', )

    subject = models.ForeignKey(to=EmailSubject,
                                verbose_name=_(u'Subject', ),
                                blank=True,
                                null=True, )

    subject_str = models.CharField(max_length=256,
                                   verbose_name=_(u'Subject str', ),
                                   blank=True,
                                   null=True, )

    template = models.ForeignKey(to=EmailTemplate,
                                 verbose_name=_(u'Template', ),
                                 blank=True,
                                 null=True, )
    template_body = models.TextField(verbose_name=_(u'Template body', ),
                                     blank=True,
                                     null=True, )

    #Дата создания и дата обновления. Устанавливаются автоматически.
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name=_(u'Дата создания', ),
                                      blank=True,
                                      null=True, )
    updated_at = models.DateTimeField(auto_now=True,
                                      verbose_name=_(u'Дата обновления', ),
                                      blank=True,
                                      null=True, )

    def __unicode__(self):
        return u'pk: %6d created_at: %s, updated_at: %s'\
               % (self.pk, self.created_at, self.updated_at, )

    class Meta:
        db_table = 'Delivery2_Message'
        ordering = ['-created_at', ]
        verbose_name = u'Рассылка отослана на (Email адрес)'
        verbose_name_plural = u'Рассылки отосланы на (Email адреса)'
