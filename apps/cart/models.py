# coding=utf-8
from django.db import models
# Create your models here.


class Cart(models.Model):
    from django.contrib.auth.models import User
    user = models.ForeignKey(User,
                             verbose_name=u'Пользователь',
                             null=True,
                             blank=True, )
    sessionid = models.CharField(verbose_name=u'SessionID',
                                 max_length=32,
                                 null=True,
                                 blank=True, )

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
        return int(summ, )

    @property
    def summ_money_of_all_products_kop(self, ):
        summ = self.summ_money_of_all_products
        summ_int = int(summ, )
        summ_float = summ - summ_int
        if summ_float > 0:
            return str('%.2f' % summ_float, ).split('.', )[1]
        else:
            return '00'

    def __unicode__(self):
        return u'Корзина пользователя:%s, SessionID:%s' % (self.user, self.sessionid, )

    class Meta:
        db_table = u'Cart'
        ordering = [u'-created_at']
        verbose_name = u'Корзина'
        verbose_name_plural = u'Корзины'


class Order(models.Model):
    from django.contrib.auth.models import User
    user = models.ForeignKey(User,
                             verbose_name=u'Пользователь',
                             null=True,
                             blank=True, )
    sessionid = models.CharField(verbose_name=u'SessionID',
                                 max_length=32,
                                 null=True,
                                 blank=True, )
    # Данные покупателя
    email = models.EmailField(verbose_name=u'E-Mail',
                              null=True,
                              blank=True, )
    FIO = models.CharField(verbose_name=u'ФИО покупателя',
                           max_length=64,
                           null=True,
                           blank=True, )
    phone = models.CharField(verbose_name=u'Номер мобильного телефона',
                             max_length=32,
                             null=True,
                             blank=True, )
    from apps.product.models import Country
    country = models.ForeignKey(Country,
                                verbose_name=u'Страна', )
    '''Если страна Украина '''
    region = models.CharField(verbose_name=u'Область',
                              max_length=64,
                              null=True,
                              blank=True, )
    settlement = models.CharField(verbose_name=u'Наименование населённого пункта',
                                  max_length=64,
                                  null=True,
                                  blank=True, )
    warehouse_number = models.CharField(verbose_name=u'Номер склада "Новой почты"',
                                        max_length=32,
                                        null=True,
                                        blank=True, )
    ''' Если страна НЕ Украина '''
    address = models.TextField(verbose_name=u'Полный адресс',
                               null=True,
                               blank=True, )
    postcode = models.CharField(verbose_name=u'Почтовый Индекс получателя',
                                max_length=12,
                                null=True,
                                blank=True, )
    ''' Комментарий к заказу '''
    comment = models.TextField(verbose_name=u'Комментарий к заказу',
                               null=True,
                               blank=True, )
    #Дата создания и дата обновления. Устанавливаются автоматически.
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True, )

    # Вспомогательные поля
    from django.contrib.contenttypes import generic
    order = generic.GenericRelation('Product',
                                    content_type_field='content_type',
                                    object_id_field='object_id', )

    @property
    def products(self, ):
        return self.order.all()

    @property
    def order_sum(self, ):
        all_products_sum = 0
        for product in self.products:
            all_products_sum += product.summ_of_quantity
        return all_products_sum

    def __unicode__(self):
        return u'Заказ пользователя:%s, SessionID:%s' % (self.user, self.sessionid, )

    class Meta:
        db_table = u'Order'
        ordering = [u'-created_at']
        verbose_name = u'Заказ'
        verbose_name_plural = u'Заказы'


class Product(models.Model):
    from django.contrib.contenttypes.models import ContentType
    content_type = models.ForeignKey(ContentType,
                                     related_name='cart',
                                     verbose_name=u'Корзина',
                                     blank=False,
                                     null=False, )
    object_id = models.PositiveIntegerField(db_index=True, )
    from django.contrib.contenttypes import generic
    key = generic.GenericForeignKey('content_type', 'object_id', )
#    cart = models.ForeignKey(Cart,
#                             related_name='cart',
#                             verbose_name=u'Корзина',
#                             null=False,
#                             blank=False, )
    from apps.product.models import Product
    product = models.ForeignKey(Product,
                                verbose_name=u'Продукт',
                                null=False,
                                blank=False, )
    quantity = models.PositiveSmallIntegerField(verbose_name=u'Количество продуктов',
                                                null=False,
                                                blank=False, )
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
    def summ_of_quantity(self, ):
        from apps.product.views import get_product
        product = get_product(product_pk=self.product_id, product_url=None, )
        return self.quantity * (self.price / product.price_of_quantity)

    def summ_quantity(self, quantity=1, ):
        """ Вызывается если дополнительные свойства карточьки продукта уже есть,
         производит сложение прошлого добавления товара с нынешним. """
        value = self.quantity + int(quantity)
        if value > 999:
            value = 999
        if value < 1:
            value = 1
        self.quantity = value
        self.save()

    def update_quantity(self, quantity=1, ):
        """ Вызывается если дополнительные свойства карточьки продукта уже есть,
         производит ИЗМЕНЕНИЕ КОЛИЧЕСТВА ТОВАРА. """
        quantity = int(quantity)
        if quantity > 999:
            quantity = 999
        elif quantity < 1:
            quantity = 1
        self.quantity = quantity
        self.save()

    def update_price_per_piece(self, ):
        """ Здесь будет расчёт цены со скидкой в зависимости от количества. """
        self.price = self.product.price
        self.save()

    @property
    def product_delete(self, ):
        """ Для начала получим саму корзину """
        product_cart = self.key
        """ Теперь нужно выяснить, "проверить", есть ли этот продукт в этой корзине ? """
        try:
            product_cart.cart.get(pk=self.pk, )
        except Product.DoesNotExist:
            """ Если нет, то возвращаем False """
            return False
        else:
            if product_cart.count_name_of_products > 1:
                """ Если продуктов в корзине много, то всё очень просто """
                self.delete()
                return product_cart
            else:
                """ Мы должны удалить продукт в корзине и саму корзину. """
                self.delete()
                product_cart.delete()
                return True

    def __unicode__(self):
        return u'Продукт в корзине:%s, количество:%d, цена:%d' % (self.product, self.quantity, self.price, )

    class Meta:
        db_table = u'Product_in_Cart'
        ordering = [u'-created_at']
        verbose_name = u'Продукт в корзине'
        verbose_name_plural = u'Продукты в корзине'
