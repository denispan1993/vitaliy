# -*- coding: utf-8 -*-
# /applications/utils/setting/models.py
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.fields import GenericRelation

from applications.product.models import Photo

__author__ = 'AlexStarov'

# Create your models here.


class Setting(models.Model):
    name = models.CharField(verbose_name=_(u'Наименование настройки', ),
                            max_length=128,
                            blank=False,
                            null=False,
                            default='', )
    variable_name = models.CharField(verbose_name=_(u'Имя переменной', ),
                                     max_length=128,
                                     unique=True,
                                     blank=False,
                                     null=False,
                                     default='', )
    description = models.TextField(verbose_name=_(u'Описание настройки', ),
                                   blank=True,
                                   null=True, )
    char = models.CharField(verbose_name=_(u'Char', ),
                            max_length=256,
                            blank=True,
                            null=True, )
    text = models.TextField(verbose_name=_(u'Text', ),
                            blank=True,
                            null=True, )
    integer = models.IntegerField(verbose_name=_(u'Integer', ),
                                  blank=True,
                                  null=True, )
    positivesmallinteger = models.PositiveSmallIntegerField(verbose_name=_(u'PositiveSmallInteger', ),
                                                            blank=True,
                                                            null=True, )

    #Дата создания и дата обновления. Устанавливаются автоматически.
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True, )
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True, )

    img = GenericRelation(
        to=Photo,
        content_type_field='content_type',
        object_id_field='object_id', )

    def __str__(self, ):
        return u'%s - %s' % (self.name, self.variable_name, )

    class Meta:
        db_table = 'Setting'
        ordering = ['created_at', ]
        verbose_name = u'Настройка'
        verbose_name_plural = u'Настройки'
