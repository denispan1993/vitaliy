# coding=utf-8
from django.db import models
from django.utils.translation import ugettext_lazy as _
from apps.product.models import Country


class Cart(models.Model):
    """
    Корзина
    """
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

    """ Расчитывает сумму всех товаров в корзине 'посчитанную' """
    def sum_money_of_all_products(self, request, ):
        all_products = self.cart.all()
        sum_money = 0
        for product in all_products:
            sum_money += float(product.sum_of_quantity(request=request, calc_or_show='calc', ), )
        return sum_money

    """ Возвращает целое число суммы корзины """
    def sum_money_of_all_products_integral(self, request, ):
        return int(self.sum_money_of_all_products(request=request, ), )

    """ Возвращает дробную часть суммы корзины """
    def sum_money_of_all_products_fractional(self, request, ):
        sum = self.sum_money_of_all_products(request=request, )
        sum_int = int(sum, )
        sum_float = sum - sum_int
        if sum_float > 0:
            return str('%.2f' % sum_float, ).split('.', )[1]
        else:
            return '00'

    def __unicode__(self):
        return u'Корзина пользователя:%s, session:%s' % (self.user, self.sessionid, )  # self.session.session_key, )

    class Meta:
        db_table = u'Cart'
        ordering = [u'-created_at']
        verbose_name = u'Корзина'
        verbose_name_plural = u'Корзины'


class Order(models.Model):
    """
    Заказ
    """
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
    country = models.ForeignKey(to=Country,
                                verbose_name=u'Страна',
                                null=True,
                                blank=True, )
    '''Если страна Украина '''
    region = models.CharField(verbose_name=u'Область',
                              max_length=64,
                              null=True,
                              blank=True, )
    settlement = models.CharField(verbose_name=u'Наименование населённого пункта',
                                  max_length=64,
                                  null=True,
                                  blank=True, )
    delivery_company = models.ForeignKey(to='DeliveryCompany',
                                         verbose_name=_(u'Компания доставщик', ),
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
    '''
        CheckBox - Я осознано сделал свой выбор и жду реквизиты для оплаты
    '''
    checkbox1 = models.BooleanField(verbose_name=u'Жду реквизиты',
                                    null=False,
                                    blank=False,
                                    default=True, )
    '''
        CheckBox - Я жду звонка менеджера
    '''
    checkbox2 = models.BooleanField(verbose_name=u'Жду звонка',
                                    null=False,
                                    blank=False,
                                    default=False, )
    recompile = models.BooleanField(verbose_name=u'Разбор Заказа',
                                    null=False,
                                    blank=False,
                                    default=False, )
    #Дата создания и дата обновления. Устанавливаются автоматически.
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True, )

    # Вспомогательные поля
    from django.contrib.contenttypes import generic
    order = generic.GenericRelation('Product',
                                    content_type_field='content_type',
                                    object_id_field='object_id', )

    @property
    def name(self, ):
        return u'Заказ № %d' % self.pk

    @property
    def products(self, ):
        return self.order.all()

    def product_add(self,
                    int_product_pk=None,
                    obj_product=None,
                    quantity=None, ):
        if not obj_product:
            from apps.product.models import Product as real_Product
            try:
                obj_product = real_Product.objects.get(pk=int_product_pk, )
            except Product.DoesNotExist:
                return self, False
        try:
            """ Присутсвие конкретного продукта в корзине """
            product_in_cart = self.order.get(product=obj_product, )
        except Product.DoesNotExist:
            """ Занесение продукта в корзину если его нету """
            if not quantity:
                quantity = obj_product.minimal_quantity
            if obj_product.is_availability == 2:  # Товар доступен под заказ
                price = obj_product.price / 2
                percentage_of_prepaid = 50
            else:
                price = obj_product.price
                percentage_of_prepaid = 100
            product_in_cart = Product.objects.create(key=self,
                                                     product=obj_product,
                                                     price=price,
                                                     # True - Товар доступен под заказ.
                                                     available_to_order=obj_product.is_availability == 2,
                                                     # 50% - предоплата.
                                                     percentage_of_prepaid=percentage_of_prepaid,
                                                     quantity=quantity, )
        else:
            if not quantity:
                quantity = obj_product.quantity_of_complete
            product_in_cart.summ_quantity(quantity, )  # quantity += exist_cart_option.quantity
            product_in_cart.update_price_per_piece()
        return self, product_in_cart

    def order_sum(self, calc_or_show='show', currency=980, ):
        all_products_sum = 0
        # from decimal import Decimal
        for product in self.products:
            all_products_sum += float(product.sum_of_quantity(calc_or_show=calc_or_show, currency=currency, ), )  # .replace('.', ',', )
        return all_products_sum

    def __unicode__(self):
        return u'Заказ пользователя:%s, SessionID:%s' % (self.user, self.sessionid, )

    class Meta:
        db_table = u'Order'
        ordering = [u'-created_at']
        verbose_name = u'Заказ'
        verbose_name_plural = u'Заказы'


class Product(models.Model):
    """
    Продукты для заказа
    """
    from django.contrib.contenttypes.models import ContentType
    content_type = models.ForeignKey(ContentType,
                                     related_name='cart_or_order',
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
    percentage_of_prepaid = models.PositiveSmallIntegerField(verbose_name=u'Процент предоплаты.',
                                                             blank=False,
                                                             null=False,
                                                             default=100,
                                                             help_text=u'Процент предоплаты за данный товар.', )
    available_to_order = models.NullBooleanField(verbose_name=u'Доступен для заказа',
                                                 default=None,
                                                 null=True,
                                                 blank=True,
                                                 help_text=u'Поле показывает, что этот товар '
                                                           u'доступен для закза. '
                                                           u'Если товар не досутпен то поле будет False. '
                                                           u'Если товар в наличии по полной стоимости, '
                                                           u'то поле будет Null', )
    #Дата создания и дата обновления. Устанавливаются автоматически.
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True, )

    def sum_of_quantity(self, request=None, calc_or_show='show', currency=980, ):
        """ Возвращаем значение суммы количества * на цену товара в текущей валюте сайта
        """
        from apps.product.views import get_product
        product = get_product(product_pk=self.product_id, product_url=None, )
        price = product.get_price(request, price=None, calc_or_show='show', currency=currency, )  # price=self.price,
        """
            Расчитываем цену товара.
        """
        from decimal import Decimal
        price = self.quantity * (Decimal(price, ) / product.price_of_quantity)
        if calc_or_show == 'calc':         # Если нас просят не просто показать, а посчитать цену товара?
            if product.is_availability == 2:  # Если товар доступен под заказ?
                """
                    Если товар доступен под заказ?
                    Показываем 50% стоимости.
                """
                price = price/2            # Берём 50% от стоимости
        return u'%5.2f'.replace(',', '.', ) % price  # .replace(',', '.', ).strip()

    def summ_quantity(self, quantity=1, ):
        """ Вызывается если дополнительные свойства карточьки продукта уже есть,
         производит сложение прошлого добавления товара с нынешним.
        """
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
        from django.db import OperationalError
        while True:
            try:
                """
                    Пытаемся записать до тех пор пока база не примет нашу запись.
                """
                self.save()
            except OperationalError as inst:
                """
                    Иначе печатаем ИЗВЕСТНУЮ ошибку
                """
                print 'Type Error: ', type(inst, )
                print 'Error: ', inst
            except Exception as inst:
                print 'Type Error: ', type(inst, )
                print 'Error: ', inst
                """
                    Иначе печатаем НЕ ИЗВЕСТНУЮ ошибку
                """
            else:
                break

    def update_price_per_piece(self, ):
        """ Здесь будет расчёт цены со скидкой в зависимости от количества. """
        if self.product.is_availability == 1:  # """ Если "Товар на складе" ТО:"""
            """ Производим расчёт цены по стандартной схеме """
            self.price = self.product.price
            self.percentage_of_prepaid = 100  # 100% стоимости товра
            self.available_to_order = None  # Товар в наличии на складе - поэтому это поле для нас не нужно
        elif self.product.is_availability == 2:  # """ Если "Товар доступен под заказ" ТО: """
            """ Считаем цену 50% от стоимости """
            self.price = self.product.price/2
            self.percentage_of_prepaid = 50  # 50% стоимости товра
            self.available_to_order = True  # Товар доступен под заказ - поэтому это поле ставим в True
        self.save()
        return self.price

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


class DeliveryCompany(models.Model, ):
    order_number = models.PositiveSmallIntegerField(verbose_name=_(u'Порядок сортировки', ),
                                                    # visibility=True,
                                                    default=1,
                                                    blank=True,
                                                    null=True, )
    select_number = models.PositiveSmallIntegerField(verbose_name=_(u'Номер в выводе', ),
                                                     # visibility=True,
                                                     default=1,
                                                     blank=True,
                                                     null=True, )
    name = models.CharField(verbose_name=_(u'Имя компании', ),
                            max_length=64,
                            null=True,
                            blank=True, )
    select_string_ru = models.CharField(verbose_name=_(u'Строка в выводе', ),
                                        max_length=64,
                                        null=True,
                                        blank=True, )
    description = models.TextField(verbose_name=_(u'Описание компании', ),
                                   null=True,
                                   blank=True, )

    #Дата создания и дата обновления. Устанавливаются автоматически.
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True, )

    def __unicode__(self):
        return u'Компания доставщик:%s, номер по порядку:%s' % (self.name, self.order_number, )

    class Meta:
        db_table = u'DeliveryCompany'
        ordering = [u'-created_at']
        verbose_name = u'Компании доставщики'
        verbose_name_plural = u'Компания доставщик'
