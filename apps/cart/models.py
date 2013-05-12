# coding=utf-8
from django.db import models
# Create your models here.


class Cart(models.Model):
    from django.contrib.auth.models import User
    user = models.ForeignKey(User, verbose_name=u'Пользователь', null=True, blank=True, )
    sessionid = models.CharField(verbose_name=u'SessionID', max_length=32, null=True, blank=True, )

    #Дата создания и дата обновления. Устанавливаются автоматически.
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True, )

    # Вспомогательные поля
    from django.contrib.contenttypes import generic
    product = generic.GenericRelation('Product',
                                      content_type_field='content_type',
                                      object_id_field='object_id', )

    @property
    def count_name_of_products(self):
        return self.cart.count()

    @property
    def sum_money_of_all_products(self):
        all_products = self.cart
        sum_money = 0
        for product in all_products:
            sum_money += product.sum_of_quantity
        return sum_money

    def __unicode__(self):
        return u'Корзина пользователя:%s, SessionID:%s' % (self.user, self.sessionid, )

    class Meta:
        db_table = u'Cart'
        ordering = [u'-created_at']
        verbose_name = u'Корзина'
        verbose_name_plural = u'Корзины'


class Product(models.Model):
    from django.contrib.contenttypes.models import ContentType
    content_type = models.ForeignKey(ContentType,
                                     related_name='cart',
                                     verbose_name=u'Корзина',
                                     blank=False,
                                     null=False, )
    object_id = models.PositiveIntegerField(db_index=True, )
    from django.contrib.contenttypes import generic
    cart = generic.GenericForeignKey('content_type', 'object_id', )
#    cart = models.ForeignKey(Cart,
#                             related_name='cart',
#                             verbose_name=u'Корзина',
#                             null=False,
#                             blank=False, )
    from apps.product.models import Product
    product = models.ForeignKey(Product, verbose_name=u'Продукт', null=False, blank=False, )
    quantity = models.PositiveSmallIntegerField(verbose_name=u'Количество продуктов', null=False, blank=False, )
    price = models.PositiveSmallIntegerField(verbose_name=u'Цена в зависимости от количества', null=True, blank=True, )

    #Дата создания и дата обновления. Устанавливаются автоматически.
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True, )

    @property
    def sum_of_quantity(self):
        return self.quantity * self.price

    def update_quantity(self, quantity=1, ):
        """ Вызывается если дополнительные свойства карточьки продукта уже есть,
         производит сложение прошлого добавления товара с нынешним. """
        value = self.quantity + int(quantity)
        if value > 999:
            value = 999
        if value < 1:
            value = 1
        self.quantity = value
        self.save()

    def update_price_per_piece(self, ):
        self.price = self.product.price
        self.save()

    def __unicode__(self):
        return u'Продукт в корзине:%s, количество:%d, цена:%d' % (self.product, self.quantity, self.price, )

    class Meta:
        db_table = u'Product_in_Cart'
        ordering = [u'-created_at']
        verbose_name = u'Продукт в корзине'
        verbose_name_plural = u'Продукты в корзине'
