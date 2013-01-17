# coding=utf-8
from django.db import models

# Create your models here.

class Cart(models.Model):
    from django.contrib.auth.models import User
    user = models.ForeignKey(User, verbose_name=u'Пользователь', null=True, blank=True, )
    sessionid = models.CharField(verbose_name=u'SessionID', max_length=32, blank=True, null=True, )

    #Дата создания и дата обновления. Устанавливаются автоматически.
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True, )

    def __unicode__(self):
        return u'Корзина пользователя:%s, SessionID:%s' % (self.user, self.sessionid, )

    class Meta:
        db_table = u'Product_in_Cart'
        ordering = [u'-created_at']
        verbose_name = u'Продукт в корзине'
        verbose_name_plural = u'Продукты в корзине'

class Product(models.Model):
    cart = models.ForeignKey(Cart, verbose_name=u'Корзина', blank=False, null=False, )
    from apps.product.models import Product
    product = models.ForeignKey(Product)
    quantity = models.PositiveSmallIntegerField(verbose_name=u'Количество продуктов', null=False, blank=False, )
    price = models.PositiveSmallIntegerField(verbose_name=u'Цена в зависимости от количества', null=True, blank=True, )

    @property
    def sum_of_quantity(self):
        return self.quantity * self.price

    #Дата создания и дата обновления. Устанавливаются автоматически.
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True, )

    def __unicode__(self):
        return u'Продукт в корзине:%s, количество:%d, цена:%d' % (self.product, self.quantity, self.price, )

    class Meta:
        db_table = u'Product_in_Cart'
        ordering = [u'-created_at']
        verbose_name = u'Продукт в корзине'
        verbose_name_plural = u'Продукты в корзине'
