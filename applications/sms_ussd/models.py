# -*- coding: utf-8 -*-
from datetime import datetime
from django.db import models
from django.utils.translation import ugettext_lazy as _
from celery.utils import uuid

import proj.settings
#from compat.bigint_path.bigint import BigIntegerField, BigForeignKey

__author__ = 'AlexStarov'


class SIM(models.Model, ):
    name = models.CharField(verbose_name=_(u'Имя устройства', ),
                            max_length=16,
                            null=True,
                            blank=True,
                            unique=True, )

    phone = models.CharField(verbose_name=_(u'Номер телефона', ),
                             max_length=14,
                             null=True,
                             blank=True, )
    provider = models.CharField(verbose_name=_(u'Провайдер', ),
                                max_length=14,
                                null=True,
                                blank=True, )
    imsi = models.BigIntegerField(verbose_name=_(u'IMSI', ),
                                  unique=True,
                                  primary_key=True,
                                  null=False,
                                  blank=False, )

    # Дата создания и дата обновления. Устанавливаются автоматически.
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name=_(u'Дата создания', ),
                                      blank=True,
                                      null=True, )
    updated_at = models.DateTimeField(auto_now=True,
                                      verbose_name=_(u'Дата обновления', ),
                                      blank=True,
                                      null=True, )

    def __unicode__(self):
        return u'%s|provider: %s ==> %s|IMSI:%s: | created_at:%s|updated_at:%s' %\
               (self.name, self.provider, self.phone, self.imsi, self.created_at, self.updated_at, )

    class Meta:
        db_table = 'SMS_USSD__SIM'
        ordering = ['-created_at', ]
        verbose_name = u'SIM'
        verbose_name_plural = u'SIM'


class SMS(models.Model, ):

    DIRECTION = (
        (1, 'Incoming', ),
        (2, 'Outgoing', ),
    )

    CODE_PROVIDER = (
        (39, '039 ==> Киевстар (Golden Telecom)',),
        (50, '050 ==> Vodafone',),
        (63, '063 ==> Life:)',),
        (66, '066 ==> Vodafone',),
        (67, '067 ==> Киевстар',),
        (68, '068 ==> Киевстар (Beeline)',),
        (91, '091 ==> Utel',),
        (92, '092 ==> PEOPLEnet',),
        (93, '093 ==> Life:)',),
        (94, '094 ==> Интертелеком',),
        (95, '095 ==> Vodafone',),
        (96, '096 ==> Киевстар',),
        (97, '097 ==> Киевстар',),
        (98, '098 ==> Киевстар',),
        (99, '099 ==> Vodafone',),
    )

    template = models.ForeignKey(to='Template',
                                 verbose_name=_(u'Template', ),
                                 null=True,
                                 blank=True, )

    direction = models.PositiveSmallIntegerField(choices=DIRECTION,
                                                 verbose_name=_(u'Направление', ),
                                                 null=True,
                                                 blank=True, )

    user = models.ForeignKey(to=proj.settings.AUTH_USER_MODEL,
                             verbose_name=_(u'Пользователь', ),
                             null=True,
                             blank=True, )
    sessionid = models.CharField(verbose_name=_(u'SessionID', ),
                                 max_length=32,
                                 null=True,
                                 blank=True, )

    task_id = models.CharField(verbose_name=_(u'task id'),
                               max_length=255,
                               blank=True,
                               null=True, )

    is_send = models.BooleanField(verbose_name=_(u'Отправлено', ),
                                  default=False,
                                  null=False,
                                  blank=True, )

    sim = models.ForeignKey(to=SIM,
                            verbose_name=_(u'SIM', ),
                            null=True,
                            blank=True, )

    from_phone_char = models.CharField(verbose_name=_(u'Номер телефона (Откуда)', ),
                                       max_length=64,
                                       null=True,
                                       blank=True, )
    from_code = models.PositiveSmallIntegerField(choices=CODE_PROVIDER,
                                                 verbose_name=_(u'Код провайдера', ),
                                                 null=True,
                                                 blank=True, )
    from_phone = models.PositiveIntegerField(verbose_name=_(u'Телефон', ),
                                             null=True,
                                             blank=True, )

    to_phone_char = models.CharField(verbose_name=_(u'Номер телефона (Куда)', ),
                                     max_length=64,
                                     null=True,
                                     blank=True, )
    to_code = models.PositiveSmallIntegerField(choices=CODE_PROVIDER,
                                               verbose_name=_(u'Код провайдера', ),
                                               null=True,
                                               blank=True, )
    to_phone = models.PositiveIntegerField(verbose_name=_(u'Телефон', ),
                                           null=True,
                                           blank=True, )

    message = models.TextField(verbose_name=_(u'Сообщение', ),
                               null=True,
                               blank=True, )
#    >> > print aaa.message.encode('cp1252', 'replace')
#    МТС Україна за змі�?т SMS не відповідає
#    123456789 123456789 123456789 1

    message_b64 = models.TextField(verbose_name=_(u'Сообщение base64', ),
                                   null=True,
                                   blank=True, )

    message_pdu = models.TextField(verbose_name=_(u'Сообщение pdu', ),
                                   null=True,
                                   blank=True, )

    send_at = models.DateTimeField(verbose_name=_(u'Дата и время отправки SMS', ),
                                   blank=True,
                                   null=True, )

    received_at = models.DateTimeField(verbose_name=_(u'Дата и время получения SMS', ),
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
        from .tasks import send_sms

        task = send_sms.apply_async(queue='delivery_send',
                                    kwargs={'sms_pk': self.pk},
                                    task_id='send_sms_celery-task-id-{0}'.format(uuid(), ), )
        self.task_id = task.id

        self.save(skip_super_save=True, )

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None, *args, **kwargs):

        skip_super_save = kwargs.pop('skip_super_save', False, )

        super(SMS, self).save(force_insert, force_update, using, update_fields, *args, **kwargs)

        if not skip_super_save:
            self.schedule_run()

    @models.permalink
    def get_absolute_url(self, ):
        return ('admin_page:sms_ussd_send_sms', (), {}, )

    def __unicode__(self):
        return u'%s:%s | direction: %s | is_send: %s: | sended_at: %s | received_at: %s' %\
               (self.user, self.sessionid, self.direction, self.is_send, self.send_at, self.received_at)

    class Meta:
        db_table = 'SMS_USSD__SMS'
        ordering = ['-created_at', ]
        verbose_name = u'SMS'
        verbose_name_plural = u'SMS'


class Template(models.Model, ):

    name = models.CharField(max_length=64,
                            unique=True,
                            verbose_name=_(u'Название', ),
                            blank=True,
                            null=True,
                            default=datetime.now, )

    is_system = models.BooleanField(verbose_name=_(u'Системный', ),
                                    default=False,
                                    null=False,
                                    blank=True, )

    template = models.TextField(verbose_name=_(u'Шаблон', ),
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

    def __unicode__(self):
        return u'%s ==> %s' % (self.name, self.is_system,)

    class Meta:
        db_table = 'SMS_USSD__Template'
        ordering = ['-created_at', ]
        verbose_name = u'Template'
        verbose_name_plural = u'Template'


class USSD(models.Model, ):

    DIRECTION = (
        (1, 'Receive', ),
        (2, 'Send',),
    )

    direction = models.PositiveSmallIntegerField(choices=DIRECTION,
                                                 verbose_name=_(u'Направление', ),
                                                 null=True,
                                                 blank=True, )

    user = models.ForeignKey(to=proj.settings.AUTH_USER_MODEL,
                             verbose_name=_(u'Пользователь', ),
                             null=True,
                             blank=True, )
    sessionid = models.CharField(verbose_name=_(u'SessionID', ),
                                 max_length=32,
                                 null=True,
                                 blank=True, )

    task_id = models.CharField(verbose_name=_(u'task.id'),
                               max_length=255,
                               blank=True,
                               null=True, )

    sim = models.ForeignKey(to=SIM,
                            verbose_name=_(u'SIM', ),
                            null=True,
                            blank=True, )

    code = models.CharField(verbose_name=_(u'USSD Code', ),
                            max_length=32,
                            null=True,
                            blank=True, )

    message = models.TextField(verbose_name=_(u'Сообщение', ),
                               null=True,
                               blank=True, )

    message_b64 = models.TextField(verbose_name=_(u'Сообщение base64', ),
                                   null=True,
                                   blank=True, )

    is_send = models.BooleanField(verbose_name=_(u'Отправлено', ),
                                  default=False,
                                  null=False,
                                  blank=True, )

    send_at = models.DateTimeField(verbose_name=_(u'Дата и время отправки USSD', ),
                                   blank=True,
                                   null=True, )

    received_at = models.DateTimeField(verbose_name=_(u'Дата и время получения USSD', ),
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
        from .tasks import send_sms

        task = send_sms.apply_async(queue='delivery_send',
                                    kwargs={'sms_pk': self.pk},
                                    task_id='send_ussd_celery-task-id-{0}'.format(uuid(), ), )
        self.task_id = task.id

        self.save(skip_super_save=True, )

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None, *args, **kwargs):

        skip_super_save = kwargs.pop('skip_super_save', False, )

        super(USSD, self).save(force_insert, force_update, using, update_fields, *args, **kwargs)

        if not skip_super_save:
            self.schedule_run()

    @models.permalink
    def get_absolute_url(self, ):
        return ('admin_page:sms_ussd_send_ussd', (), {}, )

    def __unicode__(self):
        return u'%s:%s | direction: %s | is_send: %s: | sended_at: %s | received_at: %s' %\
               (self.user, self.sessionid, self.direction, self.is_send, self.send_at, self.received_at)

    class Meta:
        db_table = 'SMS_USSD__USSD'
        ordering = ['-created_at', ]
        verbose_name = u'USSD'
        verbose_name_plural = u'USSD'
