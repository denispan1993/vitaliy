# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

import proj.settings

__author__ = 'AlexStarov'


class SendSMS(models.Model, ):

    CODE_PROVIDER = (
        (39, 'Киевстар (Golden Telecom)', ),
        (50, 'Vodafone', ),
        (63, 'Life:)', ),
        (66, 'Vodafone', ),
        (67, 'Киевстар', ),
        (68, 'Киевстар (Beeline)', ),
        (91, 'Utel', ),
        (92, 'PEOPLEnet', ),
        (93, 'Life:)', ),
        (94, 'Интертелеком', ),
        (95, 'Vodafone', ),
        (96, 'Киевстар', ),
        (97, 'Киевстар', ),
        (98, 'Киевстар', ),
        (99, 'Vodafone', ),
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

    send = models.BooleanField(verbose_name=_(u'Отправлено', ),
                               default=False,
                               null=False,
                               blank=True, )

    code = models.PositiveSmallIntegerField(choices=CODE_PROVIDER,
                                            verbose_name=_(u'Код провайдера', ),
                                            null=True,
                                            blank=True, )
    phone = models.PositiveIntegerField(verbose_name=_(u'Телефон', ),
                                        null=True,
                                        blank=True, )

    message = models.TextField(verbose_name=_(u'Сообщение', ),
                               null=True,
                               blank=True, )

    #Дата создания и дата обновления. Устанавливаются автоматически.
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name=_(u'Дата создания', ),
                                      blank=True,
                                      null=True, )
    updated_at = models.DateTimeField(auto_now=True,
                                      verbose_name=_(u'Дата обновления', ),
                                      blank=True,
                                      null=True, )

    @models.permalink
    def get_absolute_url(self, ):
        return ('admin_page:sms_ussd_send_sms', (), {}, )

    def __unicode__(self):
        return u'%s:%s' % (self.user, self.sessionid, )

    class Meta:
        db_table = 'SMS_USSD_SendSMS'
        ordering = ['-created_at', ]
        verbose_name = u'SendSMS'
        verbose_name_plural = u'SendSMS'
