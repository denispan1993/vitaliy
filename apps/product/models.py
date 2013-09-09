# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext as _

from mptt.models import MPTTModel


class Category(MPTTModel):
    from mptt import models as modelsTree
    parent = modelsTree.TreeForeignKey('Category',
                                       verbose_name=u'Вышестоящая категория',
                                       null=True,
                                       blank=True,
                                       related_name=u'children', )
    serial_number = models.PositiveSmallIntegerField(verbose_name=_(u'Порядок сортировки'),
                                                     # visibility=True,
                                                     default=1,
                                                     blank=True,
                                                     null=True, )
    is_active = models.BooleanField(verbose_name=_(u'Актив. или Пасив.'), default=True, blank=False, null=False,
                                    help_text=u'Если мы хотим чтобы категория нигде не показывалась,'
                                              u' ставим данное поле в False.')
    shown_colored = models.BooleanField(verbose_name=_(u'Выделить цветом'),
                                        default=False,
                                        blank=False,
                                        null=False,
                                        help_text=u'Если мы хотим чтобы категория была выделена цветом Фуксия,'
                                                  u' ставим данное поле в True.')
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
                                                 u' ставим данное поле в True.')
#    disclose_product = models.BooleanField(verbose_name=_(u'Открывать страницу товара'), default=True, blank=False,
#                                           null=False, help_text=u'Если мы хотим чтобы пользователь входил в товар'
#                                                                 u' со страницы категории, то ставим в True.', )
#    from compat.ruslug.models import RuSlugField
#    from apps.product.fields import ModelSlugField
    from compat.FormSlug import models as class_FormSlugField
    url = class_FormSlugField.ModelSlugField()
    #verbose_name=u'URL адрес категории', max_length=255, null=True, blank=True,
    title = models.CharField(verbose_name=u'Заголовок категории', max_length=255, null=False, blank=False, )
    # Буквы дял автоматического создания Артикула товара
    #letter_to_article = models.CharField(verbose_name=u'Буква для Артикула',
    #                                     default='CAT',
    #                                     max_length=3,
    #                                     null=False,
    #                                     blank=False,
    #                                     help_text=u'Буквы для автоматического создания Артикула товара. '
    #                                               u'Максимальнре количество букв - 3 шт.', )
    # name = models.CharField(verbose_name=u'Наименование категории', max_length=255, null=True, blank=True, )
    description = models.TextField(verbose_name=u'Описание категории', null=True, blank=True, )
    #Дата создания и дата обновления новости. Устанавливаются автоматически.
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True, )
    #Описание и ключевые слова для поисковиков
    meta_title = models.CharField(verbose_name=u'Заголовок категории', max_length=190, null=True, blank=True,
                                  help_text=u'Данный заголовок читают поисковые системы для правильного расположения'
                                            u' страницы в поиске.', )
    meta_description = models.CharField(verbose_name=u'Описание категории', max_length=190, null=True, blank=True,
                                        help_text=u'Данное описание читают поисковые системы для правильного'
                                                  u' расположения страницы в поиске.', )
    meta_keywords = models.CharField(verbose_name=u'Клчевые слова категории', max_length=160, null=True, blank=True,
                                     help_text=u'Ключевые слова для поисковых систем.', )
    #Расширенные настройки
    template = models.CharField(verbose_name=u'Имя шаблона', max_length=70, null=True, blank=True,
                                help_text=u'Пример: "news/reklama.html". Если не указано, система'
                                          u' будет использовать "news/default.html".', )
    visibility = models.BooleanField(verbose_name=u'Признак видимости категории', default=True, )

    # Вспомогательные поля
    from django.contrib.contenttypes import generic
    photo = generic.GenericRelation('Photo',
                                    content_type_field='content_type',
                                    object_id_field='object_id', )

#    from apps.product.managers import Manager
#    objects = Manager()

    objects = models.Manager()
    from apps.product import managers
    manager = managers.Manager_Category()

#    question = models.CharField(max_length=200)
#    pub_date = models.DateTimeField('date published')

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

#    @models.permalink
    def get_absolute_url(self, ):
#        return ('show_category', (),
#                {'category_url': unicode(str(self.url)),
#                 'id': unicode(str(self.pk)), }, )
        return u'/%s/к%.6d/' % (self.url, self.id, )

#    def save(self, *args, **kwargs):
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

    def __unicode__(self):
        return u'Категория: %s' % (self.title, )

    class MPTTMeta:
        level_attr = 'mptt_level'
        order_insertion_by = ['title', ]

    class Meta:
        db_table = 'Category'
        ordering = ['serial_number', '-created_at', ]
        verbose_name = u'Категория'
        verbose_name_plural = u'Категории'


class Product(models.Model):
    # id = models.AutoField(primary_key=True, db_index=True, )
    is_active = models.BooleanField(verbose_name=_(u'Актив. или Пасив.'), default=True, blank=False, null=False,
                                    help_text=u'Если мы хотим чтобы товар был пасивный, убираем галочку.')
    disclose_product = models.BooleanField(verbose_name=_(u'Открывать страницу товара'), default=True, blank=False,
                                           null=False, help_text=u'Если мы хотим чтобы пользователь входил в товар'
                                                                 u' из категории, то ставим галочку.')
    in_main_page = models.BooleanField(verbose_name=_(u'На главной странице'), default=False, blank=False, null=False,
                                       help_text=u'Если мы хотим чтобы продукт показывался на главной странице ставим'
                                                 u' данное поле в True.')
    is_bestseller = models.BooleanField(verbose_name=_(u'Магазин рекомендует'), default=False, blank=False, null=False,
                                        help_text=u'Данное поле сделано на будеющее, если вдруг когданибуть'
                                                  u' понадобится.')
    is_featured = models.BooleanField(verbose_name=_(u'Ожидается'), default=False, blank=False, null=False,
                                      help_text=u'Если мы знаем, что продукт будет доступен на складе через некоторое'
                                                u' время, ставим данное поле в True.', )
    category = models.ManyToManyField(Category, related_name=u'products', verbose_name=_(u'Категории'), blank=False,
                                      null=False, )
    from compat.FormSlug import models as class_FormSlugField
    url = class_FormSlugField.ModelSlugField(verbose_name=u'URL адрес продукта',
                                             max_length=255,
                                             null=True,
                                             blank=True, )
    title = models.CharField(verbose_name=u'Заголовок продукта', max_length=255, null=False, blank=False, )
    name = models.CharField(verbose_name=u'Наименование продукта', max_length=255, null=True, blank=True, )
    # Описание продукта
    item_description = models.CharField(verbose_name=u'Краткое описание продукта', max_length=64)
    description = models.TextField(verbose_name=u'Полное писание продукта', null=True, blank=True, )
    recomendate = models.ManyToManyField('Product',
                                         related_name=u'Product_recomendate',
                                         verbose_name=u'Рекомендуемые товары',
                                         blank=True,
                                         null=True, )
    # Минимальное количество заказа
    # minimal_quantity = models.PositiveSmallIntegerField(verbose_name=_(u'Минимальное количество заказа'), default=1,
    #                                                    blank=False, null=False, )
    minimal_quantity = models.DecimalField(verbose_name=_(u'Минимальное количество заказа'), max_digits=8,
                                           decimal_places=2, default=1, blank=False, null=False, )
    quantity_of_complete = models.DecimalField(verbose_name=_(u'Количество единиц в комплекте'), max_digits=8,
                                               decimal_places=2, default=1, blank=False, null=False, )
    weight = models.DecimalField(verbose_name=u'Вес', max_digits=8, decimal_places=2, default=0, blank=True,
                                 null=True, )
    unit_of_measurement = models.ForeignKey('Unit_of_Measurement',
                                            verbose_name=u'Единицы измерения',
                                            null=False,
                                            blank=False, )
#    Counties = (
#        (1, _('Украина', ), ),
#        (2, _('Россия', ), ),
#        (3, _('Казахстан', ), ),
#        (4, _('Белоруссия', ), ),
#        (5, _('Молдова', ), ),
#        (6, _('Приднестровье', ), ),
#    )
    Availability = (
        (1, _(u'Есть в наличии', ), ),
        (2, _(u'Ожидается', ), ),
        (3, _(u'Под заказ', ), ),
        (4, _(u'Недоступен', ), ),
    )
#    is_availability = models.BooleanField(verbose_name=_(u'Товар'),
#                                                       choices=Availability,
#                                                       default=True,
#                                                       blank=False,
#                                                       null=False, )
    is_availability = models.PositiveSmallIntegerField(verbose_name=_(u'Товар'),
                                                       choices=Availability,
                                                       default=1,
                                                       blank=False,
                                                       null=False, )
    regular_price = models.DecimalField(verbose_name=u'Обычная цена',
                                        max_digits=8,
                                        decimal_places=2,
                                        default=0,
                                        blank=True,
                                        null=True, )
    price = models.DecimalField(verbose_name=u'Цена',
                                max_digits=10,
                                decimal_places=2,
                                default=0,
                                blank=False,
                                null=False, )
    price_of_quantity = models.DecimalField(verbose_name=u'Цена за сколько?',
                                            max_digits=15,
                                            decimal_places=5,
                                            default=1,
                                            blank=False,
                                            null=False, )
    datetime_pub = models.DateTimeField(verbose_name=u'Дата публикации', null=True, blank=True, )

    #Дата создания и дата обновления. Устанавливаются автоматически.
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True, )
    #Описание и ключевые слова для поисковиков
    meta_title = models.CharField(verbose_name=u'Заголовок продукта',
                                  max_length=190,
                                  null=True,
                                  blank=True,
                                  help_text=u'Данный заголовок читают поисковые системы для правильного расположения'
                                            u' страницы в поиске.', )
    meta_description = models.CharField(verbose_name=u'Описание продукта',
                                        max_length=190,
                                        null=True,
                                        blank=True,
                                        help_text=u'Данное описание читают поисковые системы для правильного'
                                                  u' расположения страницы в поиске.', )
    meta_keywords = models.CharField(verbose_name=u'Клчевые слова продукта',
                                     max_length=160,
                                     null=True,
                                     blank=True,
                                     help_text=u'Ключевые слова для поисковых систем.', )
    #Расширенные настройки
    template = models.CharField(verbose_name=u'Имя шаблона',
                                max_length=70,
                                null=True,
                                blank=True,
                                help_text=u'Пример: "news/reklama.html". Если не указано, система будет использовать'
                                          u' "news/default.html".', )
    visibility = models.BooleanField(verbose_name=u'Признак видимости продукта',
                                     default=True, )
    # Вспомогательные поля
    from django.contrib.contenttypes import generic
    photo = generic.GenericRelation('Photo',
                                    content_type_field='content_type',
                                    object_id_field='object_id', )
    #from apps.product.models import ItemID
    ItemID = generic.GenericRelation('ItemID',
                                     content_type_field='content_type',
                                     object_id_field='object_id', )
    manufacturer = generic.GenericRelation('IntermediateModelManufacturer',
                                           content_type_field='content_type',
                                           object_id_field='object_id', )
    View = generic.GenericRelation('View',
                                   content_type_field='content_type',
                                   object_id_field='object_id', )
    Viewed = generic.GenericRelation('Viewed',
                                     content_type_field='content_type',
                                     object_id_field='object_id', )

    @property
    def content_type(self, ):
        from django.contrib.contenttypes.models import ContentType
        return ContentType.objects.get_for_model(model=self, for_concrete_model=True, )

    @property
    def get_or_create_ItemID(self, ):
#        ItemID = self.ItemID.all()
#        if ItemID:
#            return ItemID[0]
#        else:
#            from apps.product.models import ItemID
        from apps.product.models import ItemID
        from django.contrib.contenttypes.models import ContentType
        content_type = ContentType.objects.get_for_model(model=self, for_concrete_model=True, )
        try:
            ItemID = ItemID.objects.get(content_type=content_type,
                                        object_id=self.pk, )
                # parent=self, )
        except ItemID.DoesNotExist:
            manufacturer = self.manufacturer.all()
            if manufacturer:
                ItemID = ItemID.objects.create(parent=self,
                                               ItemID=u'%s-%.5d' % (manufacturer[0].key.letter_to_article.upper(),
                                                                    self.id, ), )
            else:
                ItemID = ItemID.objects.create(parent=self,
                                               ItemID=u'%.5d' % self.id, )
        return ItemID

    @property
    def get_ItemID(self, ):
        ItemID = self.ItemID.all()
        return ItemID[0].ItemID

    # Увеличение количества просмотров
    @property
    def increase_View(self, ):
        from apps.product.models import View
        from django.contrib.contenttypes.models import ContentType
        content_type = ContentType.objects.get_for_model(model=self, for_concrete_model=True, )
        try:
            View = View.objects.get(content_type=content_type,
                                    object_id=self.pk, )
        except View.DoesNotExist:
            return View.objects.create(parent=self, view_count=1, )
        else:
            View.view_count += 1
            View.save()
            return View

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
        photos = self.photo.all()
        if photos:
            return photos
        else:
            return None

#    question = models.CharField(max_length=200)
#    pub_date = models.DateTimeField('date published')

    objects = models.Manager()
    from apps.product import managers
    manager = managers.Manager_Product()

#    def save(self, *args, **kwargs): # force_insert=False, force_update=False, using=None, update_fields=None):
#        super(Product, self).save(*args, **kwargs)
#        self.create_ItemID

#    @models.permalink
    def get_absolute_url(self, ):
#        return ('show_product', (),
#                {'product_url': self.url,
#                 'id': self.pk, }, )
        return u'/%s/п%.6d/' % (self.url, self.id, )

    def cache_key(self):
        return u'%s-%.6d' % (self.slug, self.id, )

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

    def __unicode__(self):
        return u'Продукт:%s, наличие:%s' % (self.title, self.is_availability, )

    class Meta:
        db_table = 'Product'
        ordering = ['-created_at']
        verbose_name = u'Продукт'
        verbose_name_plural = u'Продукты'


class ItemID(models.Model):
    """ Ссылка на главную запись """
    from django.contrib.contenttypes.models import ContentType
    content_type = models.ForeignKey(ContentType, related_name='related_ItemID', )
    object_id = models.PositiveIntegerField(db_index=True, )
    from django.contrib.contenttypes import generic
    parent = generic.GenericForeignKey('content_type', 'object_id', )

    ItemID = models.CharField(verbose_name=u'ItemID', max_length=32, blank=True, null=True, )
    # slug = models.SlugField(verbose_name=u'Slug')
    # letter_to_article = models.CharField(verbose_name=u'Буква для Артикула', max_length=4, null=False, blank=False, )
    # Абсолютный путь к логотипу производителя
    #Дата создания и дата обновления. Устанавливаются автоматически.
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True, )

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

    def __unicode__(self):
        return self.ItemID

    class Meta:
        db_table = 'ItemID'
        ordering = ['-created_at']
        verbose_name = "Артикул продукта"
        verbose_name_plural = "Артикулы продуктов"


class IntermediateModelManufacturer(models.Model):
    """ Ссылка на главную запись """
    from django.contrib.contenttypes.models import ContentType
    content_type = models.ForeignKey(ContentType, related_name='related_Manufacturer',
                                     null=False, blank=False, default=1, )
    object_id = models.PositiveIntegerField(db_index=True,
                                            null=False, blank=False, default=1, )
    from django.contrib.contenttypes import generic
    parent = generic.GenericForeignKey('content_type', 'object_id', )
    # Собственно сам ключ на производителя
    key = models.ForeignKey('Manufacturer', verbose_name=u'Производитель', null=False, blank=False, )
    #Дата создания и дата обновления. Устанавливаются автоматически.
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True, )

    def __unicode__(self):
        return u'%.5d-%.3d-%s' % (self.pk,
                                  self.key.pk,
                                  self.key.name, )

    class Meta:
        db_table = 'IntermediateModelManufacturer'
        ordering = ['-created_at']
        verbose_name = "Ссылка на производителя"
        verbose_name_plural = "Ссылки на производителей"


class Manufacturer(models.Model):
    name = models.CharField(verbose_name=u'Название производителя', max_length=128, null=False, blank=False, )
    # slug = models.SlugField(verbose_name=u'Slug')
    letter_to_article = models.CharField(verbose_name=u'Буква для Артикула', max_length=4, null=False, blank=False, )
    # Абсолютный путь к логотипу производителя
    #Дата создания и дата обновления. Устанавливаются автоматически.
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True, )

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'Manufacturer'
        ordering = ['-created_at']
        verbose_name = "Производитель"
        verbose_name_plural = "Производители"


class Manufacturer(models.Model):
    name = models.CharField(verbose_name=u'Название производителя', max_length=128, null=False, blank=False, )
    # slug = models.SlugField(verbose_name=u'Slug')
    letter_to_article = models.CharField(verbose_name=u'Буква для Артикула', max_length=4, null=False, blank=False, )
    # Абсолютный путь к логотипу производителя
    #Дата создания и дата обновления. Устанавливаются автоматически.
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True, )

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'Manufacturer'
        ordering = ['-created_at']
        verbose_name = "Производитель"
        verbose_name_plural = "Производители"


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

    #Дата создания и дата обновления. Устанавливаются автоматически.
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True, )

    def __unicode__(self):
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

    #Дата создания и дата обновления. Устанавливаются автоматически.
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True, )

    def __unicode__(self):
        return u'Информационніе поля:%s' % (self.information, )

    class Meta:
        db_table = 'Information'
        ordering = ['-created_at']
        verbose_name = u'Информационное поле'
        verbose_name_plural = u'Информационные поля'


class Unit_of_Measurement(models.Model):
    name = models.CharField(verbose_name=u'Единица измерения',
                            max_length=64,
                            default=u'шт.',
                            null=False,
                            blank=False, )
    #Дата создания и дата обновления. Устанавливаются автоматически.
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True, )

    def __unicode__(self):
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

    #Дата создания и дата обновления. Устанавливаются автоматически.
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True, )

    def __unicode__(self):
        return u'Цены и скидки от количества:%s, количество:%d' % (self.product, self.quantity, )

    class Meta:
        db_table = 'Discount'
        ordering = ['-created_at']
        verbose_name = u'Цена и скидка'
        verbose_name_plural = u'Цены и скидки'


class Photo(models.Model):
    from django.contrib.contenttypes.models import ContentType
    content_type = models.ForeignKey(ContentType, related_name='related_Photo', )
    object_id = models.PositiveIntegerField(db_index=True, )
    from django.contrib.contenttypes import generic
    parent = generic.GenericForeignKey('content_type', 'object_id', )
    serial_number = models.PositiveIntegerField(verbose_name=u'Порядковы номер фотографии',
                                                default=1,
                                                null=False,
                                                blank=False, )
    main = models.NullBooleanField(verbose_name=u'Признак главной фотографии',
                                   null=False,
                                   blank=False,
                                   default=False, )

    def set_path_photo(self, filename):
        return 'photo/%.6d/%s' % (
            # self.product.pub_datetime.year,
            self.object_id,
            filename)
#    from compat.ImageWithThumbs.fields import ImageWithThumbsField
    from compat.ImageWithThumbs import models as class_ImageWithThumb
    photo = class_ImageWithThumb.ImageWithThumbsField(verbose_name=u'Фото',
                                                      upload_to=set_path_photo,
                                                      sizes=((90, 95), (205, 190), (210, 160), (345, 370),
                                                             (700, 500), ),
                                                      blank=False,
                                                      null=False, )
    title = models.CharField(verbose_name=u'Заголовок фотографии',
                             max_length=256,
                             null=False,
                             blank=False, )
    name = models.CharField(verbose_name=u'Наименование фотографии',
                            max_length=256,
                            null=True,
                            blank=True, )
    sign = models.CharField(verbose_name=u'Подпись sign', max_length=128, blank=True, null=True,
                            help_text=u'Подпись фотографии которая буде написана под фотографией.')
    description = models.TextField(verbose_name=u'Описание фотографии',
                                   null=True,
                                   blank=True, )
    #Дата создания и дата обновления новости. Устанавливаются автоматически.
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True, )
    #Описание и ключевые слова для поисковиков
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

    def __unicode__(self):
        return u'Фотография:%s' % (self.title, )

    class Meta:
        db_table = 'Photo'
        ordering = ['serial_number']
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

    from compat.FormSlug import models as class_FormSlugField
    url = class_FormSlugField.ModelSlugField(verbose_name=u'URL адрес страны',
                                             max_length=255,
                                             null=True,
                                             blank=True, )
    #Дата создания и дата обновления новости. Устанавливаются автоматически.
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True, )

    def __unicode__(self):
        return u'[%d] - %s' % (self.id, self.name_ru, )

    class Meta:
        db_table = 'Country'
        ordering = ['id']
        verbose_name = u'Страна'
        verbose_name_plural = u'Страны'


class View(models.Model):
    """ Ссылка на главную запись """
    from django.contrib.contenttypes.models import ContentType
    content_type = models.ForeignKey(ContentType, related_name='related_View',
                                     null=False, blank=False, default=1, )
    object_id = models.PositiveIntegerField(db_index=True,
                                            null=False, blank=False, default=1, )
    from django.contrib.contenttypes import generic
    parent = generic.GenericForeignKey('content_type', 'object_id', )

    # Количества просмотров
    view_count = models.PositiveIntegerField(verbose_name=u'Просмотров', default=1, )

    #Дата создания и дата обновления. Устанавливаются автоматически.
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True, )

    def __unicode__(self):
        return '[%.5d]: %d' % (self.id, self.view_count, )

    class Meta:
        db_table = 'View'
        ordering = ['-updated_at', ]
        verbose_name = u'Количество просмотров'
        verbose_name_plural = u'Количество просмотров'


class Viewed(models.Model):
    """ Ссылка на главную запись """
    """ Что смотрел """
    from django.contrib.contenttypes.models import ContentType
    content_type = models.ForeignKey(ContentType, related_name='related_Viewed',
                                     null=False, blank=False, default=1, )
    object_id = models.PositiveIntegerField(db_index=True,
                                            null=False, blank=False, default=1, )
    from django.contrib.contenttypes import generic
    parent = generic.GenericForeignKey('content_type', 'object_id', )
    """ Кто смотрел """
    from django.contrib.auth.models import User
    user_obj = models.ForeignKey(User, verbose_name=u'ID Пользователя', blank=True, null=True, )
    sessionid = models.CharField(verbose_name=u'SessionID', max_length=32, blank=True, null=True, )
    """ Когда смотрел """
    from datetime import datetime
    last_viewed = models.DateTimeField(verbose_name=u'Дата последнего просмотра',
                                       blank=False,
                                       null=False,
                                       default=datetime.now(), )
    #Дата создания и дата обновления. Устанавливаются автоматически.
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=u'Дата добавления', )
    updated_at = models.DateTimeField(auto_now=True, verbose_name=u'Дата последнего изменения', )

    def __unicode__(self):
        if self.user_obj:
            return '[%.5d]: %s - %s' % (self.id,
                                        self.last_viewed,
                                        self.user_obj, )
        else:
            return '[%.5d]: %s - %s' % (self.id,
                                        self.last_viewed,
                                        self.sessionid, )

    class Meta:
        db_table = 'Viewed'
        ordering = ['-updated_at', ]
        verbose_name = u'Просмотренный'
        verbose_name_plural = u'Просмотренные'


# описываем правила
from compat.FormSlug.models import ModelSlugField
from compat.ImageWithThumbs.models import ImageWithThumbsField
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
# добавляем правила и модуль
from south.modelsinspector import add_introspection_rules
add_introspection_rules(rules, ["^apps\.product\.models\.ModelSlugField"])
add_introspection_rules(rules, ["^apps\.product\.models\.ImageWithThumbsField"])

##from mptt.fields import TreeForeignKey
#from django.contrib.auth.models import Group

# add a parent foreign key
#TreeForeignKey(Category, blank=True, null=True).contribute_to_class(Category, 'parent')

#import mptt
#mptt.register(Category, order_insertion_by=['name'])
