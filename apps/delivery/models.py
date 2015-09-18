# -*- coding: utf-8 -*-
__author__ = 'Alex Starov'

from django.db import models
from django.utils.translation import ugettext_lazy as _

from datetime import date, datetime


class Delivery(models.Model, ):
    name = models.CharField(verbose_name=_(u'Имя рассылки', ),
                            max_length=128,
                            blank=True,
                            null=True,
                            default=datetime.now().isoformat(), )
    Type_Mailings = (
        (1, _(u'Акция', ), ),
        # (2, _(u'Под заказ', ), ),
        # (3, _(u'Ожидается', ), ),
        # (4, _(u'Недоступен', ), ),
    )
    delivery_test = models.BooleanField(verbose_name=_(u'Тестовая рассылка', ),
                                        blank=True,
                                        null=False,
                                        default=True, )
    type = models.PositiveSmallIntegerField(verbose_name=_(u'Тип рассылки'),
                                            choices=Type_Mailings,
                                            default=1,
                                            blank=False,
                                            null=False, )
    subject = models.CharField(verbose_name=_(u'Subject рассылки', ),
                               max_length=256,
                               blank=True,
                               null=True, )
    html = models.TextField(verbose_name=_(u'Html текст рассылки', ),
                            blank=True,
                            null=True,
                            default=10, )
    #Дата создания и дата обновления. Устанавливаются автоматически.
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name=_(u'Дата создания', ),
                                      blank=True,
                                      null=True,
                                      default=datetime.now(), )
    updated_at = models.DateTimeField(auto_now=True,
                                      verbose_name=_(u'Дата обновления', ),
                                      blank=True,
                                      null=True,
                                      default=datetime.now(), )

    @property
    def text_type(self):
        return self.Type_Mailings[self.type-1][1]

    @property
    def get_url_number(self):
        return '%06d' % self.id

    @models.permalink
    def get_absolute_url(self, ):
        return ('admin_delivery:edit',
                (),
                {'delivery_id': self.get_url_number, }, )
#                {'delivery_id': '%06d' % self.pk, }, )

    def __unicode__(self):
        # """
        # Проверка DocTest
        # >>> category = Category.objects.create(title=u'Proverka123  -ф123')
        # >>> category.item_description = u'Тоже проверка'
        # >>> category.save()
        # >>> if type(category.__unicode__()) is unicode:
        # ...     print category.__unicode__() #.encode('utf-8')
        # ... else:
        # ...     print type(category.__unicode__())
        # ...
        # Категория: Proverka123  -ф123
        # >>> print category.title
        # Proverka123  -ф123
        # """
        return u'Рассылка: № %6d - %s' % (self.pk, self.name, )

#    def save(self, *args, **kwargs):
#        from django.utils.timezone import now
#        if not self.created_at:
#            self.created_at = now()
#        self.updated_at = now()
#        return super(CouponGroup, self).save(*args, **kwargs)

    class Meta:
        db_table = 'Delivery'
        ordering = ['-created_at', ]
        verbose_name = u'Рассылка'
        verbose_name_plural = u'Рассылки'


class EmailMiddleDelivery(models.Model, ):
    delivery = models.ForeignKey(to=Delivery,
                                 verbose_name=_(u'Указатель на рассылку', ),
                                 blank=False,
                                 null=False, )
    delivery_test_send = models.BooleanField(verbose_name=_(u'Тестовая рассылка - отослана', ),
                                             blank=True,
                                             null=False,
                                             default=True, )
    delivery_send = models.BooleanField(verbose_name=_(u'Тестовая рассылка - отослана', ),
                                        blank=True,
                                        null=False,
                                        default=True, )
    #Дата создания и дата обновления. Устанавливаются автоматически.
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name=_(u'Дата создания', ),
                                      blank=True,
                                      null=True,
                                      default=datetime.now(), )
    updated_at = models.DateTimeField(auto_now=True,
                                      verbose_name=_(u'Дата обновления', ),
                                      blank=True,
                                      null=True,
                                      default=datetime.now(), )

    class Meta:
        db_table = 'EmailMiddleDelivery'
        ordering = ['-created_at', ]
        verbose_name = u'Промежуточная можель Рассылки'
        verbose_name_plural = u'Промежуточные можели Рассылок'


class EmailForDelivery(models.Model, ):
    delivery = models.ForeignKey(to=EmailMiddleDelivery,
                                 verbose_name=_(u'Указатель на рассылку', ),
                                 blank=False,
                                 null=False, )
    from apps.authModel.models import Email
    email = models.ForeignKey(to=Email,
                              verbose_name=_(u'E-Mail', ),
                              blank=False,
                              null=False, )
    send = models.BooleanField(verbose_name=_(u'Флаг отсылки', ),
                               blank=True,
                               null=False,
                               default=False, )
    #Дата создания и дата обновления. Устанавливаются автоматически.
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name=_(u'Дата создания', ),
                                      blank=True,
                                      null=True,
                                      default=datetime.now(), )
    updated_at = models.DateTimeField(auto_now=True,
                                      verbose_name=_(u'Дата обновления', ),
                                      blank=True,
                                      null=True,
                                      default=datetime.now(), )

    class Meta:
        db_table = 'EmailForDelivery'
        ordering = ['-created_at', ]
        verbose_name = u'Модель Рассылки (Email адрес)'
        verbose_name_plural = u'Модели Рассылок (Email адреса)'
