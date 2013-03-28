# coding=utf-8
from django.db import models
from django.utils.translation import ugettext as _


class Manager(models.Manager):

    def published(self):
        return self.filter(visibility=True, ).order_by('-created_at')

    def first_level(self):
        return self.filter(parent__isnull=True, )

# Create your models here.


class Category(models.Model):
    parent = models.ForeignKey(u'Category',
                               related_name='children',
                               verbose_name=u'Вышестоящая категория',
                               null=True,
                               blank=True, )
    url = models.SlugField(verbose_name=u'URL адрес категории.',
                           max_length=256,
                           null=False,
                           blank=False, )
    title = models.CharField(verbose_name=u'Заголовок категории',
                             max_length=256,
                             null=False,
                             blank=False, )
    name = models.CharField(verbose_name=u'Наименование категории',
                            max_length=256,
                            null=True,
                            blank=True, )
    description = models.TextField(verbose_name=u'Описание категории',
                                   null=True,
                                   blank=True, )
    #Дата создания и дата обновления новости. Устанавливаются автоматически.
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True, )
    #Описание и ключевые слова для поисковиков
    meta_title = models.CharField(verbose_name=u'Заголовок категории',
                                  max_length=190,
                                  null=True,
                                  blank=True,
                                  help_text=u'Данный заголовок читают поисковые системы для правильного расположения страницы в поиске.', )
    meta_description = models.CharField(verbose_name=u'Описание категории', max_length=190,
        null=True, blank=True,
                                   help_text=u'Данное описание читают поисковые системы для правильного расположения страницы в поиске.', )
    meta_keywords = models.CharField(verbose_name=u'Клчевые слова категории', max_length=160,
        null=True, blank=True,
                                help_text=u'Ключевые слова для поисковых систем.', )
    #Расширенные настройки
    template = models.CharField(verbose_name=u'Имя шаблона', max_length=70,
        null=True, blank=True,
                                help_text=u'Пример: "news/reklama.html". Если не указано, система будет использовать "news/default.html".', )
    visibility = models.BooleanField(verbose_name=u'Признак видимости категории', default=True, )

#    from apps.product.managers import Manager
#    objects = Manager()

    objects = models.Manager()
    man = Manager()

#    question = models.CharField(max_length=200)
#    pub_date = models.DateTimeField('date published')

    def get_absolute_url(self, ):
        return u'/%s/c%.6d/' % (self.url, self.id, )

#    def save(self, *args, **kwargs):
#        print(u'test1')
#        self.title += u'1'
#        if self.url == u'':
#            self.url = self.title.replace(' ', '-', )
#        super(Category, self, ).save(*args, **kwargs)

    def __unicode__(self):
        return u'Категория: %s' % (self.title, )

    class Meta:
        db_table = u'Category'
        ordering = [u'-created_at']
        verbose_name = u'Категория'
        verbose_name_plural = u'Категории'

class Product(models.Model):
    is_active = models.BooleanField(verbose_name=_(u'Показывать'),
                                    default=True,
                                    blank=False,
                                    null=False,
                                    help_text=u'Если мы хотим чтобы продукт нигде не показывался ставим данное поле в False.')
    in_main_page = models.BooleanField(verbose_name=_(u'На главной странице'),
                                       default=False,
                                       blank=False,
                                       null=False,
                                       help_text=u'Если мы хотим чтобы продукт показывался на главной странице ставим данное поле в True.')
    is_bestseller = models.BooleanField(verbose_name=_(u'Магазин рекомендует'),
                                        default=False,
                                        blank=False,
                                        null=False,
                                        help_text=u'Данное поле сделано на будеющее, если вдруг когданибуть понадобится.')
    is_availability = models.BooleanField(verbose_name=_(u'В наличии'),
                                          default=True,
                                          blank=False,
                                          null=False,
                                          help_text=u'Если мы знаем, что продукт отсутсвует на складе, ставим данное поле в False.', )
    is_featured = models.BooleanField(verbose_name=_(u'Ожидается'),
                                      default=False,
                                      blank=False,
                                      null=False,
                                      help_text=u'Если мы знаем, что продукт будет доступен на складе через некоторое время, ставим данное поле в True.', )
    category = models.ManyToManyField(Category,
                                      related_name=u'products',
                                      verbose_name=_(u'Категории'),
                                      blank=False,
                                      null=False, )
    url = models.SlugField(verbose_name=u'URL адрес продукта', max_length=128,
        null=False, blank=False, )
    title = models.CharField(verbose_name=u'Заголовок продукта', max_length=256,
        null=False, blank=False, )
    name = models.CharField(verbose_name=u'Наименование продукта', max_length=256,
        null=True, blank=True, )
    # Описание продукта
    item_description = models.CharField(verbose_name=u'Краткое описание продукта', max_length=64)
    description = models.TextField(verbose_name=u'Полное писание продукта',
        null=True, blank=True, )
    # Минимальное количество заказа
    minimal = models.PositiveSmallIntegerField(verbose_name=_(u'Минимальное количество заказа'),
                                               default=1,
                                               blank=False,
                                               null=False, )
    weight = models.DecimalField(verbose_name=u'Предположительный вес', max_digits=8, decimal_places=2, default=0, blank=True, null=True, )

    regular_price = models.DecimalField(verbose_name=u'Обычная цена', max_digits=8, decimal_places=2, default=0, blank=True, null=True, )
    price = models.DecimalField(verbose_name=u'Цена', max_digits=8, decimal_places=2, default=0, blank=False, null=False, )

    datetime_pub = models.DateTimeField(verbose_name=u'Дата публикации', null=True, blank=True, )

    #Дата создания и дата обновления. Устанавливаются автоматически.
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True, )
    #Описание и ключевые слова для поисковиков
    meta_title = models.CharField(verbose_name=u'Заголовок продукта', max_length=190,
        null=True, blank=True,
        help_text=u'Данный заголовок читают поисковые системы для правильного расположения страницы в поиске.', )
    meta_description = models.CharField(verbose_name=u'Описание продукта', max_length=190,
        null=True, blank=True,
        help_text=u'Данное описание читают поисковые системы для правильного расположения страницы в поиске.', )
    meta_keywords = models.CharField(verbose_name=u'Клчевые слова продукта', max_length=160,
        null=True, blank=True,
        help_text=u'Ключевые слова для поисковых систем.', )
    #Расширенные настройки
    template = models.CharField(verbose_name=u'Имя шаблона', max_length=70,
        null=True, blank=True,
        help_text=u'Пример: "news/reklama.html". Если не указано, система будет использовать "news/default.html".', )
    visibility = models.BooleanField(verbose_name=u'Признак видимости продукта', default=True, )

#    question = models.CharField(max_length=200)
#    pub_date = models.DateTimeField('date published')

    def get_absolute_url(self, ):
        return u'/%s/p%.6d/' % (self.url, self.id, )

    def cache_key(self):
        return u'%s-%.6d' % (self.slug, self.id, )

    def __unicode__(self):
        return u'Продукт:%s' % (self.title, )

    class Meta:
        db_table = 'Product'
        ordering = ['-created_at']
        verbose_name = u'Продукт'
        verbose_name_plural = u'Продукты'

class Additional_Information(models.Model):
    product = models.ForeignKey(Product, verbose_name=u'Продукт',
        related_name=u'information', null=False, blank=False, )
    title = models.CharField(verbose_name=u'Заголовок', null=False, blank=False, max_length=256, )

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
    additional_information = models.ForeignKey(Additional_Information, verbose_name=u'Дополнительное описание',
        null=False, blank=False, )
    information = models.CharField(verbose_name=u'Информация', null=False, blank=False, max_length=256, )

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
    name = models.CharField(verbose_name=u'Единица измерения', max_length=64, default=u'шт.',
        null=False, blank=False, )

    #Дата создания и дата обновления. Устанавливаются автоматически.
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True, )

    def __unicode__(self):
        return u'Единица измерения:%s' % (self.name, )

    class Meta:
        db_table = u'Unit_of_Measurement'
        ordering = ['-created_at']
        verbose_name = u'Единица измерения'
        verbose_name_plural = u'Единицы измерения'

class Discount(models.Model):
    product = models.ForeignKey(Product, verbose_name=u'Продукт',
        related_name=u'discount', null=False, blank=False, )
    quantity = models.DecimalField(verbose_name=u'Количество продуктов', max_digits=8, decimal_places=2,
            default=0, blank=False, null=False, )
    price = models.DecimalField(verbose_name=u'Цена в зависимости от количества', max_digits=8, decimal_places=2,
        default=0, blank=True, null=True, )
    unit_of_measurement = models.ForeignKey(Unit_of_Measurement, verbose_name=u'Единицы измерения',
        null=False, blank=False, )
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

#==================================================================================================================================
from django.db.models import ImageField
from compat.ImageWithThumbs.fields import ImageWithThumbsFieldFile

class ImageWithThumbsField(ImageField):
    attr_class = ImageWithThumbsFieldFile
    """
    Usage example:
    ==============
    photo = ImageWithThumbsField(upload_to='images', sizes=((125,125),(300,200),)

    To retrieve image URL, exactly the same way as with ImageField:
        my_object.photo.url
    To retrieve thumbnails URL's just add the size to it:
        my_object.photo.url_125x125
        my_object.photo.url_300x200

    Note: The 'sizes' attribute is not required. If you don't provide it,
    ImageWithThumbsField will act as a normal ImageField

    How it works:
    =============
    For each size in the 'sizes' atribute of the field it generates a
    thumbnail with that size and stores it following this format:

    available_filename.[width]x[height].extension

    Where 'available_filename' is the available filename returned by the storage
    backend for saving the original file.

    Following the usage example above: For storing a file called "photo.jpg" it saves:
    photo.jpg          (original file)
    photo.125x125.jpg  (first thumbnail)
    photo.300x200.jpg  (second thumbnail)

    With the default storage backend if photo.jpg already exists it will use these filenames:
    photo_.jpg
    photo_.125x125.jpg
    photo_.300x200.jpg

    Note: django-thumbs assumes that if filename "any_filename.jpg" is available
    filenames with this format "any_filename.[widht]x[height].jpg" will be available, too.

    To do:
    ======
    Add method to regenerate thubmnails

    """
    def __init__(self, verbose_name=None, name=None, width_field=None, height_field=None, sizes=None, **kwargs):
        self.verbose_name=verbose_name
        self.name=name
        self.width_field=width_field
        self.height_field=height_field
        self.sizes = sizes
        super(ImageField, self).__init__(**kwargs)
#==================================================================================================================================

class Photo(models.Model):
    from django.contrib.contenttypes.models import ContentType
    content_type = models.ForeignKey(ContentType, related_name='related_Photo', )
    object_id = models.PositiveIntegerField(db_index=True, )
    from django.contrib.contenttypes import generic
    parent = generic.GenericForeignKey('content_type', 'object_id', )
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
    photo = ImageWithThumbsField(verbose_name=u'Фото',
                                 upload_to=set_path_photo,
                                 sizes=((90,95),(205,190),(345,370),(700,500),),
                                 blank=False,
                                 null=False, )
    title = models.CharField(verbose_name=u'Заголовок фотографии',
                             max_length=256,
                             null=False,
                             blank=False, )
    name = models.CharField(verbose_name=u'Наименование фотографии', max_length=256,
        null=True, blank=True, )
    sign = models.CharField(verbose_name=u'Подпись sign', max_length=128, blank=True, null=True,
                            help_text=u'Подпись фотографии которая буде написана под фотографией.')
    description = models.TextField(verbose_name=u'Описание фотографии',
        null=True, blank=True, )

    #Дата создания и дата обновления новости. Устанавливаются автоматически.
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True, )
    #Описание и ключевые слова для поисковиков
    meta_title = models.CharField(verbose_name=u'title фотографии',
                                  max_length=190,
                                  null=True,
                                  blank=True,
                                  help_text=u'Данный title читают поисковые системы для правильного расположения фотографии в поиске.', )
    meta_alt = models.CharField(verbose_name=u'alt фотографии',
                                max_length=190,
                                null=True,
                                blank=True,
                                help_text=u'Данный alt читают поисковые системы для правильного расположения фотографии в поиске.', )

#    def get_absolute_url(self, ):
#        return '/news/rubric/%s/' % self.url

    def __unicode__(self):
        return u'Фотография:%s' % (self.title, )

    class Meta:
        db_table = 'Photo'
        ordering = ['-created_at']
        verbose_name = "Фотография"
        verbose_name_plural = "Фотографии"
