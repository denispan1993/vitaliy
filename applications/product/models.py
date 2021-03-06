# -*- coding: utf-8 -*-
from django.db import models
from datetime import datetime
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache

from mptt.models import MPTTModel, TreeForeignKey

from compat.FormSlug.models import ModelSlugField
from compat.ImageWithThumbs.models import ImageWithThumbsField

from .managers import ManagerCategory, ManagerProduct
from proj import settings

__author__ = 'AlexStarov'


def set_path_image(instance, filename, ):
    """
    Auto generate name for File and Image fields.
    :param instance: Instance of Model
    :param filename: Name of uploaded file
    :return:
    """
    import os
    import time
    import hashlib
    filename = os.path.splitext(filename)

    name = str(instance.pk or '') + filename[0] + str(time.time())

    # We think that we use utf8 based OS file system
    filename = hashlib.md5(name.encode('utf8')).hexdigest() + filename[1]
    return os.path.join('image', filename[:2], filename[2:4], filename)


class Category(MPTTModel):

    id_1c = models.CharField(verbose_name=_(u'1C Ид', ),
                             max_length=36,
                             blank=True,
                             null=True,
                             help_text=u'', )
    parent = TreeForeignKey(
        to='Category',
        verbose_name=_(u'Вышестоящая категория', ),
        null=True,
        blank=True,
        related_name='children', )

    Upper_Lower = (
        (0, _(u'Не задано', ), ),
        (1, _(u'Верх', ), ),
        (2, _(u'Низ', ), ),
    )
    location = models.PositiveSmallIntegerField(
        verbose_name=_(u'Положение'), choices=Upper_Lower,
        default=0, blank=False, null=False, )

    serial_number = models.PositiveSmallIntegerField(verbose_name=_(u'Порядок сортировки', ),
                                                     db_index=True, default=1, blank=True, null=True, )

    serial_number_left_vertical_column = models.PositiveSmallIntegerField(verbose_name=_(u'Левая вертикальная колонка', ),
                                                                          blank=True, null=True,
                                                                          help_text=u'Порядковый номер в'
                                                                                    u' левой вертикальной колонке.', )

    serial_number_first_column = models.PositiveSmallIntegerField(verbose_name=_(u'Первая колонка', ),
                                                                  db_index=True, blank=True, null=True,
                                                                  help_text=u'Порядковый номер в нижней части сайта'
                                                                            u' в первой колонке.', )

    serial_number_second_column = models.PositiveSmallIntegerField(verbose_name=_(u'Вторая колонка', ),
                                                                   db_index=True, blank=True, null=True,
                                                                   help_text=u'Порядковый номер в нижней части сайта'
                                                                             u' во второй колонке.', )

    serial_number_third_column = models.PositiveSmallIntegerField(verbose_name=_(u'Третья колонка', ),
                                                                  db_index=True, blank=True, null=True,
                                                                  help_text=u'Порядковый номер в нижней части сайта'
                                                                            u' в третьей колонке.', )

    serial_number_fourth_column = models.PositiveSmallIntegerField(verbose_name=_(u'Четвертая колонка', ),
                                                                   db_index=True, blank=True, null=True,
                                                                   help_text=u'Порядковый номер в нижней части сайта'
                                                                             u' в четвертой колонке.', )

    is_active = models.BooleanField(verbose_name=_(u'Актив. или Пасив.', ), default=True, blank=False, null=False,
                                    help_text=u'Если мы хотим чтобы категория нигде не показывалась,'
                                              u' ставим данное поле в False.', )
    shown_colored = models.BooleanField(verbose_name=_(u'Выделить цветом', ),
                                        default=False,
                                        blank=False,
                                        null=False,
                                        help_text=u'Если мы хотим чтобы категория была выделена цветом Фуксия,'
                                                  u' ставим данное поле в True.', )
    font_color = models.CharField(verbose_name=_(u'Цвет шрифта', ),
                                  max_length=32,
                                  blank=True,
                                  null=True,
                                  help_text=u'Задаем цвет шрифта категории'
                                            u'в формате "#FE45D5" или словами "Red", "Blue",', )
    shadow_color = models.CharField(verbose_name=_(u'Цвет обводки шрифта'),
                                    max_length=32,
                                    blank=True,
                                    null=True,
                                    help_text=u'Задаем цвет обводки шрифта категории'
                                              u'в формате "#FE45D5" или словами "Red", "Blue",', )
    shadow_px = models.PositiveSmallIntegerField(verbose_name=_(u'Размер обводки шрифта'),
                                                 blank=True,
                                                 null=True,
                                                 help_text=u'Задаем размер в px обводки шрифта категории', )
    # blur - размытие
    shadow_blur_px = models.PositiveSmallIntegerField(verbose_name=_(u'Размер размытия обводки шрифта'),
                                                      blank=True,
                                                      null=True,
                                                      help_text=u'Задаем размер в px размытия обводки шрифта категории', )
    shown_bold = models.BooleanField(verbose_name=_(u'Выделить жирным'),
                                     default=False,
                                     blank=False,
                                     null=False,
                                     help_text=u'Если мы хотим чтобы категория была выделена жирным шрифтом,'
                                               u' ставим данное поле в True.')
    shown_italic = models.BooleanField(verbose_name=_(u'Выделить курсивом'),
                                       default=False,
                                       blank=False,
                                       null=False,
                                       help_text=u'Если мы хотим чтобы категория была выделена наклонным шрифтом,'
                                                 u' ставим данное поле в True.', )
    font_px = models.PositiveSmallIntegerField(verbose_name=_(u'Размер шрифта'),
                                               default=14,
                                               blank=False,
                                               null=False,
                                               help_text=u'Размер шрифта категории в пикселях,', )
    # from compat.ruslug.models import RuSlugField
    # from applications.product.fields import ModelSlugField

    url = ModelSlugField()
    # verbose_name=u'URL адрес категории', max_length=255, null=True, blank=True,
    title = models.CharField(db_index=True,
                             verbose_name=u'Заголовок категории',
                             max_length=255,
                             null=False,
                             blank=False, )

    # Описание категории
    item_description = models.CharField(verbose_name=u'Краткое описание продукта',
                                        max_length=128, null=True, blank=True, )
    description = models.TextField(verbose_name=u'Описание категории', null=True, blank=True, )
    bottom_description = models.TextField(verbose_name=u'Нижнее описание категории', null=True, blank=True, )

    billboard_img = models.ImageField(verbose_name=u'Биллбоард',
                                      upload_to=set_path_image,
                                      help_text='Сюда добавляем картинку от 1920 px ширина и от 174 px высота',
                                      blank=True,
                                      null=True, )
    billboard_img_alt = models.CharField(verbose_name=u'Alt Биллбоарда',
                                         max_length=128,
                                         help_text='Описание Биллбоарда для поисковых систем от 6 до 10 слов',
                                         blank=True,
                                         null=True, )

    # Дата создания и дата обновления новости. Устанавливаются автоматически.
    created_at = models.DateTimeField(db_index=True, auto_now_add=True, )
    updated_at = models.DateTimeField(db_index=True, auto_now=True, )

    # Описание и ключевые слова для поисковиков
    meta_title = models.CharField(verbose_name=u'Заголовок категории', max_length=190, null=True, blank=True,
                                  help_text=u'Данный заголовок читают поисковые системы для правильного расположения'
                                            u' страницы в поиске.', )
    meta_description = models.CharField(verbose_name=u'Описание категории', max_length=190, null=True, blank=True,
                                        help_text=u'Данное описание читают поисковые системы для правильного'
                                                  u' расположения страницы в поиске.', )
    meta_keywords = models.CharField(verbose_name=u'Клчевые слова категории', max_length=160, null=True, blank=True,
                                     help_text=u'Ключевые слова для поисковых систем.', )
    # Расширенные настройки
    template = models.CharField(verbose_name=u'Имя шаблона', max_length=70, null=True, blank=True,
                                help_text=u'Пример: "news/reklama.html". Если не указано, система'
                                          u' будет использовать "news/default.html".', )
    visibility = models.BooleanField(verbose_name=u'Признак видимости категории', default=True, )
    # Кто создал
    # from django.contrib.auth.models import User
    user_obj = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        verbose_name=u'ID Пользователя',
        blank=True,
        null=True, )

    # Вспомогательные поля
    photo = GenericRelation(
        to='Photo',
        content_type_field='content_type',
        object_id_field='object_id', )

    objects = ManagerCategory()

    @property
    def main_photo(self, ):
        photos = self.photo.all()
        if photos:
            for photo in photos:
                if photo.main:
                    return photo
            else:
                return None
        else:
            return None

    @models.permalink
    def get_absolute_url(self, ):
        return ('show_category', (),
                {'category_url': self.url.lower() if self.url else u'категория',
                 'id': '{0:06d}'.format(self.id, ), }, )

    def save(self, *args, **kwargs):
        super(Category, self, ).save(*args, **kwargs)

##        print(u'test1')
##        self.title += u'1'
#        if self.url == u'':
#            self.url = self.title.replace(' ', '_', ).replace('$', '-', ).replace('/', '_', )
#            try:
#                existing_category = Category.objects.get(url=self.url, )
#            except Category.DoesNotExist:
##                print(u'test2')
#                super(Category, self, ).save(*args, **kwargs)
##                print(u'test3')
#                return
##                print(u'test4')
#            else:
#                self.url += '1'
##                print(u'test5')
#                super(Category, self, ).save(*args, **kwargs)
#                return
#        else:
##            print(u'test6')
#            super(Category, self, ).save(*args, **kwargs)
##            print(u'test7')
#            return

    def __str__(self):
        """
        Проверка DocTest
        >>> category = Category.objects.create(title=u'Proverka123  -ф123')
        >>> category.item_description = u'Тоже проверка'
        >>> category.save()
        >>> if type(category.__str__()) is unicode:
        ...     print category.__str__() #.encode('utf-8')
        ... else:
        ...     print type(category.__str__())
        ...
        Категория: Proverka123  -ф123
        >>> print category.title
        Proverka123  -ф123
        """
        return u'%s' % self.title

    class MPTTMeta:
        level_attr = 'mptt_level'
        order_insertion_by = ['title', ]

    class Meta:
        db_table = 'Category'
#        ordering = ['serial_number', '-created_at', ]
        ordering = ['-title', ]
        verbose_name = u'Категория'
        verbose_name_plural = u'Категории'


class Product(models.Model):
    id_1c = models.CharField(
        verbose_name=_(u'1C Ид', ),
        max_length=36,
        db_index=True,
        blank=True,
        null=True,
        help_text=u'Код 1С', )
    barcode = models.CharField(verbose_name=_(u'1C Штрихкод', ),
                               max_length=36,
                               blank=True,
                               null=True,
                               help_text=u'Штрихкод', )
    compare_with_1c = models.BooleanField(verbose_name=_(u'Сравнивать с 1C', ),
                                          default=True,
                                          help_text=u'Если стоит галочка, то этот товар сравнивается по параметрам с 1С', )

    is_active = models.BooleanField(verbose_name=_(u'Актив. или Пасив.'), default=True, blank=False, null=False,
                                    help_text=u'Если мы хотим чтобы товар был пасивный, убираем галочку.')
    disclose_product = models.BooleanField(verbose_name=_(u'Открывать страницу товара'), default=True, blank=False,
                                           null=False, help_text=u'Если мы хотим чтобы пользователь входил в товар'
                                                                 u' из категории, то ставим галочку.')
    in_main_page = models.BooleanField(db_index=True,
                                       verbose_name=_(u'На главной странице'), default=False, blank=False, null=False,
                                       help_text=u'Если мы хотим чтобы продукт показывался на главной странице ставим'
                                                 u' данное поле в True.')
    is_bestseller = models.BooleanField(verbose_name=_(u'Магазин рекомендует'), default=False, blank=False, null=False,
                                        help_text=u'Данное поле сделано на будеющее, если вдруг когданибуть'
                                                  u' понадобится.')
    is_featured = models.BooleanField(verbose_name=_(u'Ожидается'), default=False, blank=False, null=False,
                                      help_text=u'Если мы знаем, что продукт будет доступен на складе через некоторое'
                                                u' время, ставим данное поле в True.', )
    category = models.ManyToManyField(Category,
                                      related_name=u'products',
                                      verbose_name=_(u'Категории'),
                                      through='ProductToCategory',
                                      through_fields=('product', 'category', ),
                                      blank=False, )
    serial_number = models.PositiveSmallIntegerField(
        verbose_name=_(u'Порядок сортировки'),
        # visibility=True,
        db_index=True,
        default=1,
        blank=True,
        null=True, )
    url = ModelSlugField(
        db_index=True,
        verbose_name=u'URL адрес продукта',
        max_length=255,
        null=True,
        blank=True, )
    title = models.CharField(
        verbose_name=u'Заголовок продукта',
        max_length=255,
        db_index=True,
        null=False,
        blank=False, )
    name = models.CharField(
        verbose_name=u'Наименование продукта',
        max_length=255,
        db_index=True,
        null=True,
        blank=True, )

    # Описание продукта
    item_description = models.CharField(verbose_name=u'Краткое описание продукта',
                                        max_length=128, )  # null=True, blank=True, )
    description = models.TextField(verbose_name=u'Полное описание продукта',
                                   null=True, blank=True, )
    # recommended recomendate
    recommended = models.ManyToManyField('Product',
                                         related_name=u'Product',
                                         verbose_name=u'Рекомендуемые товары',
                                         blank=True, )
    # Минимальное количество заказа
    minimal_quantity = models.DecimalField(verbose_name=_(u'Минимальное количество заказа'), max_digits=8,
                                           decimal_places=2, default=1, blank=False, null=False, )
    quantity_of_complete = models.DecimalField(verbose_name=_(u'Количество единиц в комплекте'), max_digits=8,
                                               decimal_places=2, default=1, blank=False, null=False, )
    weight = models.DecimalField(verbose_name=u'Вес', max_digits=8, decimal_places=2, default=0, blank=True,
                                 null=True, )
    unit_of_measurement = models.ForeignKey('UnitofMeasurement',
                                            verbose_name=u'Единицы измерения',
                                            null=False,
                                            blank=False, )
    Availability = (
        (1, _(u'Есть в наличии', ), ),
        (2, _(u'Под заказ', ), ),
        (3, _(u'Ожидается', ), ),
        (4, _(u'Недоступен', ), ),
    )
    is_availability = models.IntegerField(verbose_name=_(u'Наличие'),
                                          choices=Availability,
                                          default=1,
                                          blank=False,
                                          null=False, )
    quantity_in_stock = models.IntegerField(verbose_name=_(u'Количество на складе'),
                                            blank=False,
                                            null=False,
                                            default=0, )
    """ Акции """
    from applications.discount.models import Action
    action = models.ManyToManyField(to=Action,
                                    verbose_name=_('Акции'),
                                    related_name='product_in_action',
                                    blank=True,  #  null=True,
                                    db_table='Product_to_Action', )
    in_action = models.BooleanField(verbose_name=_('Продукт учавствует в Акции'),
                                    blank=False,
                                    null=False,
                                    default=False, )
    regular_price = models.DecimalField(verbose_name=_('Обычная цена'),
                                        max_digits=8,
                                        decimal_places=2,
                                        default=0,
                                        blank=True,
                                        null=True, )
    currency = models.ForeignKey('Currency',
                                 verbose_name=_('Валюта'),
                                 blank=False,
                                 null=False,
                                 default=1, )
    price = models.DecimalField(verbose_name=_('Цена', ),
                                max_digits=10,
                                decimal_places=2,
                                default=0,
                                blank=False,
                                null=False, )
    action_price = models.DecimalField(verbose_name=_('Акционная цена', ),
                                       max_digits=10,
                                       decimal_places=2,
                                       default=0,
                                       blank=False,
                                       null=False, )
    price_of_quantity = models.DecimalField(verbose_name=_('Цена за сколько?'),
                                            max_digits=15,
                                            decimal_places=5,
                                            default=1,
                                            blank=False,
                                            null=False, )
    datetime_pub = models.DateTimeField(verbose_name=u'Дата публикации', null=True, blank=True, )

    # Дата создания и дата обновления. Устанавливаются автоматически.
    created_at = models.DateTimeField(db_index=True, auto_now_add=True, )
    updated_at = models.DateTimeField(db_index=True, auto_now=True, )

    # Описание и ключевые слова для поисковиков
    meta_title = models.CharField(verbose_name=u'Заголовок продукта',
                                  max_length=190,
                                  null=True,
                                  blank=True,
                                  help_text=u'Данный заголовок читают поисковые системы для правильного расположения '
                                            u'страницы в поиске.<br>'
                                            u'Оптимальная длинна то 15 до 80 символов без учёта пробела.', )
    meta_description = models.CharField(verbose_name=u'Описание продукта',
                                        max_length=190,
                                        null=True,
                                        blank=True,
                                        help_text=u'Данное описание читают поисковые системы для правильного '
                                                  u'расположения страницы в поиске.<br>'
                                                  u'Оптимальная длинна от 70 до 160 символов с учётом пробелов.', )
    meta_keywords = models.CharField(verbose_name=u'Клчевые слова продукта',
                                     max_length=160,
                                     null=True,
                                     blank=True,
                                     help_text=u'Ключевые слова для поисковых систем.<br>'
                                               u'Перечисляются через запятую без пробелов.<br>'
                                               u'Еслю ключевое слово сосотит из двух слов'
                                               u' то между ними ставится пробел<br>'
                                               u'Общая длина ключевых слов не должна превышать 1000 символов.', )

    check_index_date = models.DateTimeField(verbose_name=u'Дата и время последней проверки индексации страницы',
                                            blank=True,
                                            null=True, )
    in_yandex = models.NullBooleanField(verbose_name=u'Yandex. В индексе',
                                        blank=True,
                                        null=True, )
    in_google = models.NullBooleanField(verbose_name=u'Google. В индексе',
                                        blank=True,
                                        null=True, )

    # Расширенные настройки
    template = models.CharField(verbose_name=u'Имя шаблона',
                                max_length=70,
                                null=True,
                                blank=True,
                                help_text=u'Пример: "news/reklama.html". Если не указано, система будет использовать'
                                          u' "news/default.html".', )
    visibility = models.BooleanField(verbose_name=u'Признак видимости продукта',
                                     default=True, )
    # Кто создал
    # from django.contrib.auth.models import User
    user_obj = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        verbose_name=u'ID Пользователя',
        blank=True,
        null=True, )
    # Вспомогательные поля
    photo = GenericRelation(
        to='Photo',
        content_type_field='content_type',
        object_id_field='object_id', )
    # from applications.product.models import ItemID
    ItemID = GenericRelation(
        to='ItemID',
        content_type_field='content_type',
        object_id_field='object_id', )
    manufacturer = GenericRelation(
        to='IntermediateModelManufacturer',
        content_type_field='content_type',
        object_id_field='object_id', )
    View = GenericRelation(
        to='View',
        content_type_field='content_type',
        object_id_field='object_id', )
    Viewed = GenericRelation(
        to='Viewed',
        content_type_field='content_type',
        object_id_field='object_id', )
    from applications.comment.models import Comment
    comments = GenericRelation(
        to=Comment,
        content_type_field='content_type',
        object_id_field='object_id', )

    @property
    def content_type(self, ):
        return ContentType.objects.get_for_model(model=self, for_concrete_model=True, )

    @property
    def recomendation(self, ):
        """ Вернуть все рекоммендованные товары с учётом их наличия на складе """
        """ Перемешать вывод https://docs.djangoproject.com/en/dev/ref/models/querysets/#order-by-fields """
        return self.recommended.filter(is_availability=1, ).order_by('?')

    def get_or_create_ItemID(self, itemid=None):
        try:
            if itemid:
                return ItemID.objects.get(
                    content_type=self.content_type,
                    object_id=self.pk,
                    ItemID=itemid, )
            else:
                return ItemID.objects.get(
                    content_type=self.content_type,
                    object_id=self.pk, )
        except ItemID.DoesNotExist:
            manufacturer = self.manufacturer.all()
            if itemid:
                return ItemID.objects.create(content_type=self.content_type,
                                             object_id=self.pk,
                                             ItemID=itemid, )
            elif manufacturer:
                return ItemID.objects.create(content_type=self.content_type,
                                             object_id=self.pk,
                                             ItemID=u'%s-%.5d' % (manufacturer[0].key.letter_to_article.upper(),
                                                                  self.pk, ), )
            else:
                return ItemID.objects.create(content_type=self.content_type,
                                             object_id=self.pk,
                                             ItemID=u'%.5d' % self.pk, )
        except ItemID.MultipleObjectsReturned:
            manufacturer = self.manufacturer.all()
            ItemIDs = ItemID.objects.filter(content_type=self.content_type,
                                            object_id=self.pk, )
            for i, inst_ItemID in enumerate(ItemIDs):

                if i + 1 == len(ItemIDs):
                    return inst_ItemID

                if inst_ItemID.ItemID == u'%.5d' % self.pk\
                        or (len(manufacturer) > 0
                            and inst_ItemID.ItemID == u'%s-%.5d' % (
                                    manufacturer[0].key.letter_to_article.upper(),
                                    self.pk, )
                            ):
                    inst_ItemID.delete()

    @property
    def get_ItemID(self, ):
        """ Взять артикул товара """
        ItemID = self.ItemID.all()
        try:
            return ItemID[0].ItemID
        except IndexError:
            return self.get_or_create_ItemID().ItemID

    @property
    def get_manufacturer(self, ):
        """ Взять производителя товара """
        manufacturer = self.manufacturer.all()
        if manufacturer:
            manufacturer = manufacturer[0].key
            if manufacturer.name and manufacturer.name is '' or not manufacturer.name:
                return manufacturer.country.name_ru
            elif manufacturer.name and manufacturer.name is not '':
                return u'%s (%s)' % (manufacturer.name, manufacturer.country.name_ru, )
            else:
                return None
        else:
            return None

    # Увеличение количества просмотров
    # @property
    def increase_View(self, ):
        from applications.product.models import View
        try:
            View = View.objects.get(content_type=self.content_type,
                                    object_id=self.pk, )
        except View.DoesNotExist:
            return View.objects.create(parent=self, view_count=1, )
        else:
            from django.db.models import F
            View.view_count = F('view_count') + 1
            # View.view_count += 1
            # View.save()
            # return View
            return View.objects.get(content_type=self.content_type,
                                    object_id=self.pk, )

#    def increase_view(self):
##        self.view_count = self.view_count + 1
##        self.save()
#        try:
#            views = Counters.objects.get(news=self, )
#        except Counters.DoesNotExist:
#            views = Counters.objects.create(news=self, viewers=1, )
#            return 1
#        else:
#            from django.db.models import F
#            views.viewers = F('viewers') + 1
#            views.save() #update_fields=['views_count']
#            return Counters.objects.get(news=self, ).viewers

    @property
    def main_photo(self, ):
        photos = self.photo.all()
        if photos:
            for photo in photos:
                if photo.main:
                    return photo
            else:
                return None
        else:
            return None

    @property
    def all_photos(self, ):
        photos = self.photo.all().order_by('serial_number', '-created_at')
        if photos:
            return photos
        else:
            return None

    def get_category_hierarchy(self, request=None, ):
        if request:
            current_category = request.session.get('current_category', None, )

            if current_category:
                try:
                    current_category = Category.objects.get(pk=current_category, )

                    s = current_category.title

                    while current_category.parent:
                        current_category = current_category.parent
                        s = u'{0}/{1}'.format(current_category.title, s)

                    return s

                except Category.DoesNotExist:
                    pass

        return ''

    def get_price(self, request=None, price=None, calc_or_show='show', currency_ISO_number=None, ):
        currency_pk = 1

        if request:

            currency_pk = request.session.get(u'currency_pk', )
            if currency_pk:
                try:
                    currency_pk = int(currency_pk, )
                except ValueError:
                    pass

        elif not request and currency_ISO_number:

            key = 'currency_{0}'.format(currency_ISO_number, )
            print('(get_price) key: ', key, )
            currency = cache.get(key=key, )
            if not currency:
                try:
                    currency = Currency.objects.get(currency_code_ISO_number=currency_ISO_number, )
                    print('(get_price) not key for code_ISO_number: ', currency.currency_code_ISO_number, )
                    cache.set(
                        key=key,
                        value=currency,
                        timeout=3600, )  # 60 sec * 60 min
                    currency_pk = currency.pk
                    current_currency_object = currency
                except Currency.DoesNotExist:
                    pass
            else:
                currency_pk = currency.pk
                current_currency_object = currency

        if 'current_currency_object' not in locals()\
                and (self.currency_id != 1 or currency_pk != 1):

            current_currency_object = cache.get(key='currency_pk_{0}'.format(currency_pk, ), )
            if not current_currency_object:
                try:
                    current_currency_object = Currency.objects.get(pk=currency_pk, )
                    print('(get_price) not key for code_currency_pk: ', current_currency_object.pk, )
                    cache.set(
                        key='currency_pk_{0}'.format(currency_pk, ),
                        value=current_currency_object,
                        timeout=3600, )  # 60 sec * 60 min
                except Currency.DoesNotExist:
                    pass
        print('0', price)
        if not price:
            if self.in_action:
                price = self.action_price
                print('1', price)
            else:
                price = self.price
                print('2.0', self.price)
                print('2', price)
        print('3', price)
        if 'current_currency_object' in locals():
            current_currency_pk = current_currency_object.pk
            current_currency = current_currency_object.currency
            current_exchange_rate = current_currency_object.exchange_rate

            product_currency_pk = self.currency_id

            product_currency_obj = cache.get(key='currency_pk_{0}'.format(product_currency_pk, ), )
            if not product_currency_obj:
                product_currency_obj = self.currency
                cache.set(
                    key='currency_pk_{0}'.format(self.currency_id, ),
                    value=product_currency_obj,
                    timeout=3600, )  # 60 sec * 60 min

            product_currency = product_currency_obj.currency

            product_exchange_rate = product_currency_obj.exchange_rate
            if current_currency_pk == 1 and product_currency_pk != 1:
                ''' Приводим к гривне:
                    1. цену делим на количество гривен
                    2. умножаем на курс '''
                price = price/product_currency*product_exchange_rate
                ''' Округляем до целого значения '''
                price = round(price, )
            elif current_currency_pk == 2 and product_currency_pk != 2:
                ''' Сначала приводим к гривне '''
                intermediate_price = price/product_currency*product_exchange_rate
                ''' Приводим к 2-ой валюте сайта (Рублю) '''
                price = intermediate_price*current_currency/current_exchange_rate
                ''' Округляем до целого значения '''
                price = round(price, )
            elif current_currency_pk != 1 and product_currency_pk == 1:
                ''' Приводим к нужной валюте:
                    1. умножаем на количество гривен
                    2. делим на курс '''
                price = price*current_currency/current_exchange_rate
            elif current_currency_pk != 1 and product_currency_pk != 1:
                ''' Сначала приводим к гривне '''
                intermediate_price = price/product_currency*product_exchange_rate
                ''' Приводим к текущей валюте сайта '''
                price = intermediate_price*current_currency/current_exchange_rate
        print(price)
        if calc_or_show == 'calc':         # Если нас просят не просто показать, а посчитать цену товара?
            if self.is_availability == 2:  # Если товар доступен под заказ?
                price = price/2            # Берём 50% от стоимости
        return u'%5.2f'.replace(',', '.', ).strip() % price

    def check_product_availability(self, product_cart='product', ):
        if self.is_availability == 1:
            return 1, u''
        elif self.is_availability == 2:
            if product_cart == 'product':
                return 2, u'Товар доступен под заказ'
            elif product_cart == 'cart':
                return 2, u'Товар под заказ (предоплата 50%)'
            elif product_cart == 'order':
                return 2, u'Товар под заказ (предоплата 50%)'
        elif self.is_availability == 3:
            return 3, u'Товар ожидается'
        elif self.is_availability == 4:
            return 4, u'<strong>Товар недоступен.</strong><br>Рекоммендуем его удалить из корзины.'

    # objects = models.Manager()
    # manager = managers.Manager_Product()
    objects = ManagerProduct()

#    def save(self, *args, **kwargs): # force_insert=False, force_update=False, using=None, update_fields=None):
#        super(Product, self).save(*args, **kwargs)
#        self.create_ItemID

#    @models.permalink
##    def get_absolute_url(self, ):
#        return ('show_product', (),
#                {'product_url': self.url,
#                 'id': self.pk, }, )
#        if self.url:
#            return u'/%s/п%.6d/' % (self.url.lower(), self.id, )
#        else:
#            return None
##        return u'/%s/п%.6d/' % (self.url.lower() if self.url else u'продукт', self.id, )

    @models.permalink
    def get_absolute_url(self, ):
        return ('show_product', (),
                {'product_url': self.url.lower() if self.url else u'продукт',
                 'id': '{0:06d}'.format(self.id, ), }, )

    def cache_key(self, ):
        return u'%s-%.6d' % (self.url.lower(), self.id, )

#    def save(self, *args, **kwargs):
##        print(u'test1')
##        self.title += u'1'
#        if self.url == u'':
#            self.url = self.title.replace(' ', '_', ).replace('$', '-', ).replace('/', '_', )
#            try:
#                existing_pruduct = Product.objects.get(url=self.url, )
#            except Product.DoesNotExist:
#                super(Product, self, ).save(*args, **kwargs)
#                return
#            else:
#                self.url += '1'
#                super(Product, self, ).save(*args, **kwargs)
#                return
#        else:
#            super(Product, self, ).save(*args, **kwargs)
#            return

    def __str__(self):
        return u'Продукт:%s' % self.title

    class Meta:
        db_table = 'Product'
        # ordering = ['serial_number', '-created_at', ]
        ordering = ['-created_at', ]
        verbose_name = u'Продукт'
        verbose_name_plural = u'Продукты'


class ProductToCategory(models.Model):
    product = models.ForeignKey(Product, )
    category = models.ForeignKey(Category, )
    is_main = models.BooleanField(verbose_name=_(u'Главная категория', ),
                                  default=False, )

    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True, )

    class Meta:
        unique_together = ('product', 'category', )
        db_table = 'ProductToCategory'


class ItemID(models.Model):
    """ Ссылка на главную запись """
    content_type = models.ForeignKey(ContentType, related_name='related_ItemID', )
    object_id = models.PositiveIntegerField(db_index=True, )
    parent = GenericForeignKey('content_type', 'object_id', )

    ItemID = models.CharField(
        verbose_name=u'ItemID',
        max_length=32,
        db_index=True,
        blank=True,
        null=True, )
    # slug = models.SlugField(verbose_name=u'Slug')
    # letter_to_article = models.CharField(verbose_name=u'Буква для Артикула', max_length=4, null=False, blank=False, )
    # Дата создания и дата обновления. Устанавливаются автоматически.
    created_at = models.DateTimeField(db_index=True, auto_now_add=True, )
    updated_at = models.DateTimeField(db_index=True, auto_now=True, )

#    def save(self, *args, **kwargs): # force_insert=False, force_update=False, using=None, update_fields=None):
#        """ В базе в теории в одну еденицу времени есть только один экземпляр ItemID """
#        """ пытаемся взять этот экземпляр """
#        try:
#            old_ItemID = ItemID.objects.get(object_id=self.object_id,
#                                            content_type_id=self.content_type_id, )
#        except ItemID.DoesNotExist:
#            old_ItemID = None
#        if not old_ItemID:
#            """ Пишем новый, если в базе пусто """
#            super(ItemID, self).save(*args, **kwargs)
#        else:
#            #print('self.pk: %s' % self.pk, )
#            #print('self.ItemID: %s' % self.ItemID, )

#            #print('old_ItemID.pk: %d' % old_ItemID.pk, )
#            #print('old_ItemID.ItemID: %s' % old_ItemID.ItemID, )
#            ''' Проверяем: Экземпляр, который уже есть в базе
#             является автоматическим ItemID ? '''
#            if not old_ItemID.ItemID == u'%.5d' % self.parent.pk: # and \
#               # old_ItemID.pk == self.pk:
#                # print('super save not Empty')
#                old_ItemID.delete()
#                super(ItemID, self).save(*args, **kwargs)
#            if not old_ItemID.ItemID == self.ItemID and \
#               old_ItemID.pk == self.pk:
#                super(ItemID, self).save(*args, **kwargs)

    def __str__(self):
        return self.ItemID

    class Meta:
        db_table = 'ItemID'
        ordering = ['-created_at']
        verbose_name = "Артикул продукта"
        verbose_name_plural = "Артикулы продуктов"


class IntermediateModelManufacturer(models.Model):
    """ Промежуточная модель 'производитель' """
    """ Ссылка на главную запись """
    content_type = models.ForeignKey(ContentType, related_name='related_Manufacturer',
                                     null=False, blank=False, default=1, )
    object_id = models.PositiveIntegerField(db_index=True,
                                            null=False, blank=False, default=1, )
    parent = GenericForeignKey('content_type', 'object_id', )
    # Собственно сам ключ на производителя
    key = models.ForeignKey('Manufacturer',
                            verbose_name=u'Производитель',
                            null=False, blank=False, )
    # Дата создания и дата обновления. Устанавливаются автоматически.
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True, )

    def __str__(self):
        manufacturer = self.key
        country = manufacturer.country
        if manufacturer.name:
            return u'%.5d-%.3d-%.2d %s (%s)' % (self.pk,
                                                manufacturer.pk,
                                                country.pk,
                                                manufacturer.name,
                                                country.name_ru, )
        else:
            return u'%.5d-%.3d-%.2d (%s)' % (self.pk,
                                             manufacturer.pk,
                                             country.pk,
                                             country.name_ru, )

    class Meta:
        db_table = 'IntermediateModelManufacturer'
        ordering = ['-created_at']
        verbose_name = u"Ссылка на производителя"
        verbose_name_plural = u"Ссылки на производителей"


class Manufacturer(models.Model):
    """ Модель 'производитель' """
    country = models.ForeignKey('Country',
                                verbose_name=u'Страна производитель',
                                null=False,
                                blank=False,
                                default=1, )
    name = models.CharField(verbose_name=u'Наименование производителя',
                            max_length=128,
                            null=True,
                            blank=True,
                            default='', )
    # slug = models.SlugField(verbose_name=u'Slug')
    letter_to_article = models.CharField(verbose_name=u'Буква для Артикула',
                                         max_length=4,
                                         null=False,
                                         blank=False, )
    # Абсолютный путь к логотипу производителя
    # Дата создания и дата обновления. Устанавливаются автоматически.
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True, )

    def __str__(self):
        if self.name:
            return u'%s (%s)' % (self.name, self.country.name_ru, )
        else:
            return self.country.name_ru  # .decode(encoding='utf-8', )

    class Meta:
        db_table = 'Manufacturer'
        ordering = ['-created_at']
        verbose_name = u"Производитель"
        verbose_name_plural = u"Производители"

#
#class Manufacturer(models.Model):
#    name = models.CharField(verbose_name=u'Название производителя', max_length=128, null=False, blank=False, )
#    # slug = models.SlugField(verbose_name=u'Slug')
#    letter_to_article = models.CharField(verbose_name=u'Буква для Артикула', max_length=4, null=False, blank=False, )
#    # Абсолютный путь к логотипу производителя
#    #Дата создания и дата обновления. Устанавливаются автоматически.
#    created_at = models.DateTimeField(auto_now_add=True, )
#    updated_at = models.DateTimeField(auto_now=True, )
#
#    def __str__(self):
#        return self.name
#
#    class Meta:
#        db_table = 'Manufacturer'
#        ordering = ['-created_at']
#        verbose_name = "Производитель"
#        verbose_name_plural = "Производители"


class Additional_Information(models.Model):
    product = models.ForeignKey(Product,
                                verbose_name=_(u'Продукт'),
                                related_name=u'information',
                                null=False,
                                blank=False, )
    title = models.CharField(verbose_name=_(u'Заголовок'),
                             null=False,
                             blank=False,
                             max_length=255, )
#    informations = models.ManyToManyField(Information,
#                                          verbose_name=_(u'Информационные поля'),
#                                          blank=False,
#                                          null=False, )

    # Дата создания и дата обновления. Устанавливаются автоматически.
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True, )

    def __str__(self):
        return u'Дополнительная информация:%s' % (self.title, )

    class Meta:
        db_table = 'Additional_Information'
        ordering = ['-created_at']
        verbose_name = u'Дополнительная информация'
        verbose_name_plural = u'Дополнительная информация'


class Information(models.Model):
    additional_information = models.ForeignKey(Additional_Information,
                                               verbose_name=u'Дополнительное описание',
                                               null=False,
                                               blank=False, )
    information = models.CharField(verbose_name=u'Информация',
                                   null=False,
                                   blank=False,
                                   max_length=255, )

    # Дата создания и дата обновления. Устанавливаются автоматически.
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True, )

    def __str__(self):
        return u'Информационные поля:%s' % (self.information, )

    class Meta:
        db_table = 'Information'
        ordering = ['-created_at']
        verbose_name = u'Информационное поле'
        verbose_name_plural = u'Информационные поля'


class UnitofMeasurement(models.Model):
    name = models.CharField(verbose_name=u'Единица измерения',
                            max_length=64,
                            default=u'шт.',
                            null=False,
                            blank=False, )
    # Дата создания и дата обновления. Устанавливаются автоматически.
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True, )

    def __str__(self):
        return u'%s' % (self.name, )

    class Meta:
        db_table = u'Unit_of_Measurement'
        ordering = ['-created_at']
        verbose_name = u'Единица измерения'
        verbose_name_plural = u'Единицы измерения'


class Discount(models.Model):
    product = models.ForeignKey(Product, verbose_name=u'Продукт',
                                related_name=u'discount',
                                null=False,
                                blank=False, )
    quantity = models.DecimalField(verbose_name=u'Количество продуктов',
                                   max_digits=8,
                                   decimal_places=2,
                                   default=0,
                                   blank=False,
                                   null=False, )
    price = models.DecimalField(verbose_name=u'Цена в зависимости от количества',
                                max_digits=8,
                                decimal_places=2,
                                default=0,
                                blank=True,
                                null=True, )
    percent = models.PositiveSmallIntegerField(verbose_name=u'Процент скидки', null=True, blank=True, )

    # Дата создания и дата обновления. Устанавливаются автоматически.
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True, )

    def __str__(self):
        return u'Цены и скидки от количества:%s, количество:%d' % (self.product, self.quantity, )

    class Meta:
        db_table = 'Discount'
        ordering = ['-created_at']
        verbose_name = u'Цена и скидка'
        verbose_name_plural = u'Цены и скидки'


def set_path_photo(self, filename):
    return 'photo/%.6d/%s' % (
        # self.product.pub_datetime.year,
        self.object_id,
        filename)


class Photo(models.Model):
    content_type = models.ForeignKey(ContentType, related_name='related_Photo', )
    object_id = models.PositiveIntegerField(db_index=True, )
    parent = GenericForeignKey('content_type', 'object_id', )
    serial_number = models.PositiveIntegerField(verbose_name=u'Порядковы номер фотографии',
                                                db_index=True,
                                                default=1,
                                                null=False,
                                                blank=False, )
    main = models.NullBooleanField(verbose_name=u'Признак главной фотографии',
                                   null=False,
                                   blank=False,
                                   default=False, )

    # from compat.ImageWithThumbs.fields import ImageWithThumbsField
    photo = ImageWithThumbsField(
        verbose_name=u'Фото',
        upload_to=set_path_photo,
        sizes=((26, 26, ), (50, 50, ), (90, 95, ),
               (205, 190, ), (210, 160, ), (253, 228, ), (345, 370, ),
               (700, 500, ), ),
        blank=False,
        null=False, )
    title = models.CharField(verbose_name=u'Заголовок фотографии',
                             max_length=256,
                             null=True,
                             blank=True,
                             help_text=u'title <a> записи.')
    name = models.CharField(verbose_name=u'Наименование фотографии',
                            max_length=256,
                            null=True,
                            blank=True, )
    sign = models.CharField(verbose_name=u'Подпись sign', max_length=128, blank=True, null=True,
                            help_text=u'Подпись фотографии которая буде написана под фотографией.')
    description = models.TextField(verbose_name=u'Описание фотографии',
                                   null=True,
                                   blank=True, )
    # Дата создания и дата обновления новости. Устанавливаются автоматически.
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True, )
    # Описание и ключевые слова для поисковиков
    meta_title = models.CharField(verbose_name=u'title фотографии',
                                  max_length=190,
                                  null=True,
                                  blank=True,
                                  help_text=u'Данный title читают поисковые системы для правильного расположения'
                                            u' фотографии в поиске.', )
    meta_alt = models.CharField(verbose_name=u'alt фотографии',
                                max_length=190,
                                null=True,
                                blank=True,
                                help_text=u'Данный alt читают поисковые системы для правильного расположения'
                                          u' фотографии в поиске.', )

#    def get_absolute_url(self, ):
#        return '/news/rubric/%s/' % self.url

    def __str__(self):
        return u'Фотография:%s' % (self.title, )

    class Meta:
        db_table = 'Photo'
        ordering = ['serial_number', '-created_at', ]
        verbose_name = "Фотография"
        verbose_name_plural = "Фотографии"


class Country(models.Model):
    name_ru = models.CharField(verbose_name=u'Название страны Russian',
                               max_length=64,
                               blank=False,
                               null=False, )
    name_en = models.CharField(verbose_name=u'Название страны English',
                               max_length=50,
                               blank=False,
                               null=False, )
    phone_code = models.PositiveIntegerField(verbose_name=u'Телефонный код страны без +',
                                             blank=True,
                                             null=True, )
    url = ModelSlugField(
        verbose_name=u'URL адрес страны',
        max_length=255,
        null=True,
        blank=True, )
    # Дата создания и дата обновления. Устанавливаются автоматически.
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True, )

    def __str__(self):
        return u'[%d] - %s' % (self.id, self.name_ru, )

    class Meta:
        db_table = 'Country'
        ordering = ['id']
        verbose_name = u'Страна'
        verbose_name_plural = u'Страны'


class Region(models.Model):
    country = models.ForeignKey(to=Country,
                                verbose_name=_(u'Страна', ),
                                blank=False,
                                null=False,
                                default=1, )
    name_ru = models.CharField(verbose_name=u'Название области Russian',
                               max_length=64,
                               blank=False,
                               null=False, )
    name_en = models.CharField(verbose_name=u'Название области English',
                               max_length=50,
                               blank=False,
                               null=False, )
    url = ModelSlugField(
        verbose_name=u'URL адрес страны',
        max_length=255,
        null=True,
        blank=True, )
    # Дата создания и дата обновления. Устанавливаются автоматически.
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True, )

    def __str__(self):
        return u'[%d] - %s' % (self.id, self.name_ru, )

    class Meta:
        db_table = 'Region'
        ordering = ['id']
        verbose_name = u'Область'
        verbose_name_plural = u'Области'


class City(models.Model):
    region = models.ForeignKey(to=Region,
                               verbose_name=_(u'Область', ),
                               blank=False,
                               null=False,
                               default=1, )
    name_ru = models.CharField(verbose_name=u'Название города Russian',
                               max_length=64,
                               blank=False,
                               null=False, )
    name_en = models.CharField(verbose_name=u'Название города English',
                               max_length=50,
                               blank=False,
                               null=False, )
    phone_code = models.PositiveIntegerField(verbose_name=u'Телефонный код города',
                                             blank=True,
                                             null=True, )
    url = ModelSlugField(
        verbose_name=u'URL адрес страны',
        max_length=255,
        null=True,
        blank=True, )

    # Дата создания и дата обновления. Устанавливаются автоматически.
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True, )

    def __str__(self):
        return u'[%d] - %s' % (self.id, self.name_ru, )

    class Meta:
        db_table = 'City'
        ordering = ['id']
        verbose_name = u'Город'
        verbose_name_plural = u'Города'


class Currency(models.Model):
    """
        Валюта
    """
    country = models.ForeignKey('Country',
                                verbose_name=u'Принадлежность валюты',
                                null=True, blank=True, default=1, )
    name_ru = models.CharField(verbose_name=u'Название валюты Russian',
                               max_length=16, blank=False, null=False, )
    currency_code_ISO_number = models.PositiveSmallIntegerField(db_index=True,
                                                                verbose_name=_(u'Код валюты числовой', ),
                                                                blank=False,
                                                                null=False,
                                                                default=0, )
    currency_code_ISO_char = models.CharField(verbose_name=_(u'Код валюты буквенный', ),
                                              max_length=3,
                                              blank=False,
                                              null=False,
                                              default='UAH', )
    currency_code_char = models.CharField(verbose_name=_(u'Код валюты код', ),
                                          max_length=1,
                                          blank=False,
                                          null=False,
                                          default=u'₴', )
    name_truncated = models.CharField(verbose_name=u'Название валюты сокращенный',
                                      max_length=8, blank=True, null=True, )
    name_en = models.CharField(verbose_name=u'Название валюты English',
                               max_length=16, blank=False, null=False, )
    """ Курс обмена валюты """
    currency = models.DecimalField(verbose_name=u'Количество валюты для обмена',
                                   max_digits=12, decimal_places=5,
                                   blank=False, null=False, default=1,
                                   help_text=u'Сколько нужно обменять валюты', )
    exchange_rate = models.DecimalField(verbose_name=u'Курс обмена в Гривнах',
                                        max_digits=12, decimal_places=5,
                                        blank=False, null=False, default=1,
                                        help_text=u'Сколько дают за эту валюту в Гривнах', )
    # Дата создания и дата обновления. Устанавливаются автоматически.
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True, )

    def __str__(self):
        return u'[%d] - %s (%s)' % (self.pk, self.name_ru, self.name_en, )

    class Meta:
        db_table = 'Currency'
        ordering = ['id']
        verbose_name = u'Валюта'
        verbose_name_plural = u'Валюты'


class View(models.Model):
    """
        Сколько раз просмотрели товар или категорию.
    """
    """ Ссылка на главную запись """
    content_type = models.ForeignKey(ContentType, related_name='related_View',
                                     null=False, blank=False, default=1, )
    object_id = models.PositiveIntegerField(db_index=True,
                                            null=False, blank=False, default=1, )
    parent = GenericForeignKey('content_type', 'object_id', )

    # Количества просмотров
    view_count = models.PositiveIntegerField(verbose_name=u'Просмотров', default=1, )

    # Дата создания и дата обновления. Устанавливаются автоматически.
    created_at = models.DateTimeField(db_index=True, auto_now_add=True, )
    updated_at = models.DateTimeField(db_index=True, auto_now=True, )

    def __str__(self):
        return '[%.5d]: %d' % (self.id, self.view_count, )

    class Meta:
        db_table = 'View'
        ordering = ['-updated_at', ]
        verbose_name = u'Количество просмотров'
        verbose_name_plural = u'Количество просмотров'


class Viewed(models.Model):
    """ Какие товары посмотрел пользователь. """
    """ Ссылка на главную запись """
    content_type = models.ForeignKey(ContentType, related_name='related_Viewed',
                                     null=False, blank=False, default=1, )
    object_id = models.PositiveIntegerField(db_index=True,
                                            null=False, blank=False, default=1, )

    parent = GenericForeignKey('content_type', 'object_id', )
    """ Кто смотрел """
    user_obj = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        verbose_name=u'ID Пользователя',
        blank=True,
        null=True, )
    sessionid = models.CharField(verbose_name=u'SessionID',
                                 db_index=True, max_length=32, blank=True, null=True, )
    """ Когда смотрел """
    last_viewed = models.DateTimeField(verbose_name=u'Дата последнего просмотра',
                                       db_index=True, blank=False, null=False,
                                       default=timezone.now, )

    # Дата создания и дата обновления. Устанавливаются автоматически.
    created_at = models.DateTimeField(db_index=True, auto_now_add=True, verbose_name=u'Дата добавления', )
    updated_at = models.DateTimeField(db_index=True, auto_now=True, verbose_name=u'Дата последнего изменения', )

    def __str__(self):
        try:
            pk = int(self.pk, )
        except TypeError:
            pk = 1
        if self.user_obj:
            return '[%.5d]: %s - %s' % (pk,
                                        self.last_viewed,
                                        self.user_obj, )
        else:
            return '[%.5d]: %s - %s' % (pk,
                                        self.last_viewed,
                                        self.sessionid, )

    class Meta:
        db_table = 'Viewed'
        ordering = ['-updated_at', ]
        verbose_name = u'Просмотренный'
        verbose_name_plural = u'Просмотренные'

# Extended Price


class InformationForPrice(models.Model):
    product = models.ForeignKey(
        to=Product,
        verbose_name=_(u'Продукт', ),
        related_name='informationforprice',
        null=True,
        blank=True, )
    information = models.CharField(verbose_name=_(u'Информация', ),
                                   max_length=255,
                                   null=False,
                                   blank=False, )

    # Дата создания и дата обновления. Устанавливаются автоматически.
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True, )

    def __str__(self):
        return self.information

    class Meta:
        db_table = 'InformationForPrice'
        ordering = ['-created_at']
        verbose_name = u'Информационное поле для прайса'
        verbose_name_plural = u'Информационные поля для прайса'


class ExtendedPrice(models.Model):
    product = models.ForeignKey(
        to=Product,
        verbose_name=_(u'Продукт', ),
        related_name='extendedprice',
        null=False,
        blank=False, )
    information = models.ManyToManyField(InformationForPrice,
                                         verbose_name=_(u'Информация', ),
                                         blank=False, )
    regular_price = models.DecimalField(verbose_name=_(u'Старая цена', ),
                                        max_digits=10,
                                        decimal_places=2,
                                        default=0,
                                        blank=True,
                                        null=True, )
    price = models.DecimalField(verbose_name=_(u'Цена', ),
                                max_digits=10,
                                decimal_places=2,
                                default=0,
                                blank=False,
                                null=False, )

    # Дата создания и дата обновления. Устанавливаются автоматически.
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True, )

    def __str__(self):
        return u'%s' % (self.price, )

    class Meta:
        db_table = u'ExtendedPrice'
        ordering = ['-created_at']
        verbose_name = u'Расширеная цена'
        verbose_name_plural = u'Расширение цен'


class AdditionalInformationForPrice(models.Model):
    product = models.ForeignKey(Product,
                                verbose_name=_(u'Продукт'),
                                related_name='additionalinformationforprice',
                                null=False,
                                blank=False, )
    title = models.CharField(verbose_name=_(u'Заголовок'),
                             null=False,
                             blank=False,
                             max_length=255, )
    information = models.ManyToManyField(InformationForPrice,
                                         # through='AdditionalInformationAndInformationForPrice',
                                         verbose_name=_(u'Информация для прайса', ),
                                         blank=False, )
    # price = models.ManyToManyField(ExtendedPrice,
    #                                verbose_name=_(u'Прайс', ),
    #                                null=False,
    #                                blank=False, )

    # Дата создания и дата обновления. Устанавливаются автоматически.
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True, )

    def __str__(self):
        return u'Дополнительная информация для прайса:%s' % (self.title, )

    # def save(self, *args, **kwargs):
    #     print(self.title)
    #     print(self.product)
#        self.information.save_m2m()
        # all_informations = self.information.all()
        # print(all_informations)
        # print(self.information)
        # for inf in all_informations:
        #     print inf.information
    #     super(AdditionalInformationForPrice, self, ).save(*args, **kwargs)
##        print(u'test1')
##        self.title += u'1'
#        if self.url == u'':
#            self.url = self.title.replace(' ', '_', ).replace('$', '-', ).replace('/', '_', )
#            try:
#                existing_category = Category.objects.get(url=self.url, )
#            except Category.DoesNotExist:
##                print(u'test2')
#                super(Category, self, ).save(*args, **kwargs)
##                print(u'test3')
#                return
##                print(u'test4')
#            else:
#                self.url += '1'
##                print(u'test5')
#                super(Category, self, ).save(*args, **kwargs)
#                return
#        else:
##            print(u'test6')
#            super(Category, self, ).save(*args, **kwargs)
##            print(u'test7')
#            return

    class Meta:
        db_table = 'AdditionalInformationForPrice'
        ordering = ['-created_at']
        verbose_name = u'Дополнительная информация для прайса'
        verbose_name_plural = u'Дополнительная информация для прайса'


# описываем правила
rules = [
    (
        (ModelSlugField, ), [],
        {
            "null": ["null", {"default": False}],
            "blank": ["blank", {"default": False}],
        }
    ),
    (
        (ImageWithThumbsField, ), [],
        {
            "null": ["null", {"default": False}],
            "blank": ["blank", {"default": False}],
        }
    ),
]
## добавляем правила и модуль
#from south.modelsinspector import add_introspection_rules
#add_introspection_rules(rules, ["^applications\.product\.models\.ModelSlugField"])
#add_introspection_rules(rules, ["^applications\.product\.models\.ImageWithThumbsField"])

##from mptt.fields import TreeForeignKey
#from django.contrib.auth.models import Group

# add a parent foreign key
#TreeForeignKey(Category, blank=True, null=True).contribute_to_class(Category, 'parent')

#import mptt
#mptt.register(Category, order_insertion_by=['name'])


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True, report=True, )
#    doctest.testfile("test.txt")
    #doctest.testfile("test.txt",verbose=True)
