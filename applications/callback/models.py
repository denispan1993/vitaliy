# -*- coding: utf-8 -*-
__author__ = 'Alex Starov'
from django.db import models
from django.utils.translation import ugettext_lazy as _
# Create your models here.


class CallBack(models.Model):
    """ Обратный звонок """
    # from django.contrib.auth.models import User
    from proj.settings import AUTH_USER_MODEL
    user = models.ForeignKey(to=AUTH_USER_MODEL,
                             verbose_name=u'Пользователь',
                             null=True,
                             blank=True, )
    # from django.contrib.sessions.models import Session
    # session = models.ForeignKey(to=Session,
    #                             verbose_name=u'Session Foreign_Key',
    #                             null=True,
    #                             blank=True, )
    sessionid = models.CharField(verbose_name=u'SessionID',
                                 max_length=32,
                                 null=True,
                                 blank=True, )

    #Дата создания и дата обновления. Устанавливаются автоматически.
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True, )

    # Поля введенные пользователем
    name = models.CharField(max_length=64,
                            verbose_name=_(u'Имя оставившего просьбу "обратный звонок"', ),
                            blank=True,
                            null=True, )
    phone = models.CharField(max_length=32,
                             verbose_name=_(u'Номер телефона', ),
                             blank=False,
                             null=False,
                             default='phone number', )
    email = models.EmailField(verbose_name=_(u'E-Mail', ),
                              blank=True,
                              null=True, )

    def __str__(self):
        return u'Обратный звонок:%s, session:%s' % (self.user, self.sessionid, )  # self.session.session_key, )

    class Meta:
        db_table = u'CallBack'
        ordering = [u'-created_at']
        verbose_name = u'Обратный звонок'
        verbose_name_plural = u'Обратные звонки'
