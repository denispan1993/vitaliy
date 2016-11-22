# -*- coding: utf-8 -*-
# /apps/delivery2/models.py

import os
import time
import hashlib
from celery.result import AsyncResult
from celery.utils import uuid

from django.db import models, IntegrityError
from django.utils.translation import ugettext_lazy as _
from datetime import datetime, timedelta
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.template.loader import render_to_string
from django.db.models import Q

from compat.ImageWithThumbs import models as class_ImageWithThumb
from apps.utils.captcha.views import key_generator
from apps.cart.models import Order
from apps.authModel.models import Email as authModel_Email
from apps.delivery.models import SpamEmail as delivery_Email

__author__ = 'AlexStarov'


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
    basedir = os.path.join(instance._meta.app_label, instance._meta.module_name)
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

    template = models.ForeignKey(to='EmailTemplate',
                                 related_name='delivery_EmailTemplate',
                                 verbose_name=_(u'Template', ),
                                 blank=True,
                                 null=True, )

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

        print self.task_id
        print self.is_active
        print self.started_at
        if not kwargs.pop('skip_schedule', False):
            print self.started_at.replace(tzinfo=None) > datetime.now()

        if not kwargs.pop('skip_schedule', True)\
                and not self.task_id\
                and not self.is_active\
                and self.started_at\
                and self.started_at.replace(tzinfo=None) > datetime.now():
            print 'Uraaaaaaaaaaaa!!!!!!!!!!'
            print self.started_at.replace(tzinfo=None)
            print datetime.now()
            self.schedule_run()

        super(Delivery, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'Рассылка: № %6d: %s' % (self.pk, self.name, )

    class Meta:
        db_table = 'Delivery2_Delivery'
        ordering = ['-created_at', ]
        verbose_name = u'Рассылка'
        verbose_name_plural = u'Рассылки'


class Subject(models.Model, ):
    delivery = models.ForeignKey(to=Delivery,
                                 blank=False,
                                 null=False,)

    subject = models.CharField(verbose_name=_(u'Тема письма', ),
                               max_length=256,
                               blank=False,
                               null=False,
                               default=_(u'Тема', ), )

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
        db_table = 'Delivery2_Subject'
        ordering = ['-created_at', ]
        verbose_name = _(u'Тема', )
        verbose_name_plural = _(u'Темы', )


class EmailTemplate(models.Model, ):
    """ template будующей рассылки """
    delivery = models.ForeignKey(to=Delivery,
                                 blank=False,
                                 null=False, )

    template = models.FileField(upload_to=upload_to, verbose_name=u'Шаблон')

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
        return u'Тело письма: № %6d: %2.2f' % (self.pk, self.chance)

    class Meta:
        db_table = 'Delivery2_Template'
        ordering = ['-created_at', ]
        verbose_name = _(u'Тело письма', )
        verbose_name_plural = _(u'Тема писем', )


class RedirectUrl(models.Model, ):
    """ Связка URL в письме и куда будет редирект """
    id = models.BigIntegerField(primary_key=True, )

    delivery = models.ForeignKey(to=Delivery,
                                 verbose_name=_(u'Рассылка'),
                                 blank=False,
                                 null=False,)

    href = models.CharField(verbose_name=_(u'URL', ),
                            max_length=256,
                            blank=False,
                            null=False,
                            default='http://keksik.com.ua/', )

    uuid = models.CharField(verbose_name=_(u'UUID', ),
                            max_length=256,
                            blank=False,
                            null=False,
                            default='http://keksik.com.ua/', )

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
        return u'pk:%0.6d [href:%s]' % (self.pk, self.href, )

    class Meta:
        db_table = 'Delivery2_RedirectUrl'
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

    subject = models.ForeignKey(to=Subject,
                                verbose_name=_(u'Указатель на subject', ),
                                blank=True,
                                null=True, )

    subject_str = models.CharField(max_length=256,
                                   verbose_name=_(u'Строка subject', ),
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
