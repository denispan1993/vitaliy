# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext as _


class Price_Additional_Information(models.Model):
    from apps.product.models import Product
    product = models.ForeignKey(Product,
                                verbose_name=_(u'Продукт'),
                                related_name=u'price_additional_information',
                                null=False,
                                blank=False, )
    title = models.CharField(verbose_name=_(u'Заголовок'),
                             null=False,
                             blank=False,
                             max_length=255, )

    #Дата создания и дата обновления. Устанавливаются автоматически.
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True, )

    def __unicode__(self):
        return u'Дополнительная информация для прайса:%s' % (self.title, )

    class Meta:
        db_table = 'Price_Additional_Information'
        ordering = ['-created_at']
        verbose_name = u'Дополнительная информация для прайса'
        verbose_name_plural = u'Дополнительная информация для прайса'


class Price_Information(models.Model):
    from apps.product.models import Product
    product = models.ForeignKey(Product,
                                verbose_name=_(u'Продукт'),
                                related_name=u'price_information',
                                null=False,
                                blank=False, )
    additional_information = models.ForeignKey(Price_Additional_Information,
                                               verbose_name=u'Дополнительное описание для прайса',
                                               null=False,
                                               blank=False, )
    information = models.CharField(verbose_name=u'Информация для прайса',
                                   null=False,
                                   blank=False,
                                   max_length=255, )

    #Дата создания и дата обновления. Устанавливаются автоматически.
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True, )

    def __unicode__(self):
        return u'Информационные поля для прайса:%s' % (self.information, )

    class Meta:
        db_table = 'Price_Information'
        ordering = ['-created_at']
        verbose_name = u'Информационное поле для прайса'
        verbose_name_plural = u'Информационные поля для прайса'


class Extended_Price(models.Model):
    price_informations = models.ManyToManyField(Price_Information,
                                                verbose_name=_(u'Информационные поля для прайса'),
                                                blank=False,
                                                null=False, )
    price = models.DecimalField(verbose_name=u'Цена в зависимости от выбранных критериев',
                                max_digits=8,
                                decimal_places=2,
                                default=0,
                                blank=True,
                                null=True, )
    #Дата создания и дата обновления. Устанавливаются автоматически.
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True, )

    def __unicode__(self):
        return u'%s' % (self.price, )

    class Meta:
        db_table = u'Extended_Price'
        ordering = ['-created_at']
        verbose_name = u'Цена в зависимости от выбранных критериев'
        verbose_name_plural = u'Цены в зависимости от выбранных критериев'
