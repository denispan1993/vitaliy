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
    cart = generic.GenericRelation('Product',
                                   content_type_field='content_type',
                                   object_id_field='object_id', )

    @property
    def products(self, ):
        return self.cart.all()

    @property
    def count_name_of_products(self, ):
        return self.cart.count()

    @property
    def summ_money_of_all_products(self, ):
        all_products = self.cart.all()
        summ_money = 0
        for product in all_products:
            summ_money += product.summ_of_quantity
        return summ_money

    @property
    def summ_money_of_all_products_grn(self, ):
        summ = self.summ_money_of_all_products
        return int(summ)

    @property
    def summ_money_of_all_products_kop(self, ):
        summ = self.summ_money_of_all_products
        return str(summ - int(summ, ), ).split('.', )[1]

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
    price = models.DecimalField(verbose_name=u'Цена в зависимости от количества',
                                max_digits=8,
                                decimal_places=2,
                                default=0,
                                blank=False,
                                null=False, )
    #Дата создания и дата обновления. Устанавливаются автоматически.
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True, )

    @property
    def summ_of_quantity(self):
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
        """ Здесь будет расчёт цены со скидкой в зависимости от количества. """
        self.price = self.product.price
        self.save()

    def __unicode__(self):
        return u'Продукт в корзине:%s, количество:%d, цена:%d' % (self.product, self.quantity, self.price, )

    class Meta:
        db_table = u'Product_in_Cart'
        ordering = [u'-created_at']
        verbose_name = u'Продукт в корзине'
        verbose_name_plural = u'Продукты в корзине'
