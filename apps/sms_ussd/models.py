# -*- coding: utf-8 -*-
from datetime import datetime
from django.db import models
from django.utils.translation import ugettext_lazy as _
from celery.utils import uuid

import proj.settings

__author__ = 'AlexStarov'


class SMS(models.Model, ):

    CODE_PROVIDER = (
        (39, '039 ==> Киевстар (Golden Telecom)', ),
        (50, '050 ==> Vodafone', ),
        (63, '063 ==> Life:)', ),
        (66, '066 ==> Vodafone', ),
        (67, '067 ==> Киевстар', ),
        (68, '068 ==> Киевстар (Beeline)', ),
        (91, '091 ==> Utel', ),
        (92, '092 ==> PEOPLEnet', ),
        (93, '093 ==> Life:)', ),
        (94, '094 ==> Интертелеком', ),
        (95, '095 ==> Vodafone', ),
        (96, '096 ==> Киевстар', ),
        (97, '097 ==> Киевстар', ),
        (98, '098 ==> Киевстар', ),
        (99, '099 ==> Vodafone', ),
    )

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

    from_phone_char = models.CharField(verbose_name=_(u'Номер телефона (Откуда)', ),
                                       max_length=16,
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
                                     max_length=16,
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

        if not kwargs.pop('skip_super_save', False):
            self.schedule_run()

        kwargs.pop('skip_super_save', None)

        super(SMS, self).save(force_insert, force_update, using, update_fields, *args, **kwargs)

    @models.permalink
    def get_absolute_url(self, ):
        return ('admin_page:sms_ussd_send_sms', (), {}, )

    def __unicode__(self):
        return u'%s:%s' % (self.user, self.sessionid, )

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
