# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _


class WaitList(models.Model):
    is_send = models.BooleanField(verbose_name=_(u'Оповещение отослано - Да или Нет', ),
                                  default=False,
                                  blank=True,
                                  null=True, )
    from apps.authModel.models import Email
    email = models.ForeignKey(to=Email,
                              verbose_name=_(u'Ссылка на E-Mail адрес', ),
                              blank=False,
                              null=False, )
    from apps.product.models import Product
    product = models.ForeignKey(to=Email,
                                verbose_name=_(u'Ссылка на ожидаемый продукт', ),
                                blank=False,
                                null=False, )
    #Дата создания и дата обновления. Устанавливаются автоматически.
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True, )

    class Meta:
        db_table = 'WaitlList'
#        ordering = ['serial_number', '-created_at', ]
        ordering = ['-created_at', ]
        verbose_name = u'Список Ожидания'
        verbose_name_plural = u'Списки Ожиданий'
