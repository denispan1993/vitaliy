# coding=utf-8
from django.db import models

# Create your models here.

class Category(models.Model):
    parent = models.ForeignKey(u'Category', verbose_name=u'Вышестоящая категория',
        related_name=u'children', null=True, blank=True, )
    url = models.SlugField(verbose_name=u'URL адрес категории.', max_length=128,
        null=False, blank=False, )
    title = models.CharField(verbose_name=u'Заголовок категории', max_length=256,
        null=False, blank=False, )
    name = models.CharField(verbose_name=u'Наименование категории', max_length=256,
        null=True, blank=True, )
    description = models.TextField(verbose_name=u'Описание категории',
        null=True, blank=True, )

    #Дата создания и дата обновления новости. Устанавливаются автоматически.
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True, )
    #Описание и ключевые слова для поисковиков
    meta_title = models.CharField(verbose_name=u'Заголовок категории', max_length=190,
        null=True, blank=True,
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

    from apps.product.managers import Manager
    objects = Manager()

#    question = models.CharField(max_length=200)
#    pub_date = models.DateTimeField('date published')

    def get_absolute_url(self, ):
        return u'/%s/c%.6d/' % (self.url, self.id, )

    def __unicode__(self):
        return u'Категория:%s' % (self.title, )

    class Meta:
        db_table = 'Category'
        ordering = ['-created_at']
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

class Product(models.Model):
    is_active = models.BooleanField(verbose_name=u'Показывать', default=True,
                                   help_text=u'Если мы хотим чтобы продукт нигде не показывался ставим данное поле в False.')
    in_main_page = models.BooleanField(verbose_name=u'На главной странице', default=False,
                                   help_text=u'Если мы хотим чтобы продукт показывался на главной странице ставим данное поле в True.')
    is_bestseller = models.BooleanField(verbose_name=u'Магазин рекомендует', default=False,
                                   help_text=u'Данное поле сделано на будеющее, если вдруг когданибуть понадобится.')
    is_featured = models.BooleanField(verbose_name=u'Ожидается', default=False,
                                   help_text=u'Если мы знаем, что продукт будет доступен на складе через некоторое время, ставим данное поле в True.')
    category = models.ManyToManyField(Category, verbose_name=u'Категории',
        related_name=u'product', null=False, blank=False, )
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
    weight = models.DecimalField(verbose_name=u'Предположительный вес', max_digits=8, decimal_places=2, default=0, blank=True, null=True, )

    #Дата создания и дата обновления новости. Устанавливаются автоматически.
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

    def __unicode__(self):
        return u'Продукт:%s' % (self.title, )

    class Meta:
        db_table = 'Product'
        ordering = ['-created_at']
        verbose_name = u'Продукт'
        verbose_name_plural = u'Продукты'

#=================================================================================================================================================================================
# -*- encoding: utf-8 -*-
"""
django-thumbs by Antonio Melé
http://django.es
"""
from django.db.models import ImageField
from django.db.models.fields.files import ImageFieldFile
from PIL import Image
from django.core.files.base import ContentFile
import cStringIO

def generate_thumb(img, thumb_size, format):
    """
    Generates a thumbnail image and returns a ContentFile object with the thumbnail

    Parameters:
    ===========
    img         File object

    thumb_size  desired thumbnail size, ie: (200,120)

    format      format of the original image ('jpeg','gif','png',...)
                (this format will be used for the generated thumbnail, too)
    """

    img.seek(0) # see http://code.djangoproject.com/ticket/8222 for details
    image = Image.open(img)

    # Convert to RGB if necessary
    if image.mode not in ('L', 'RGB', 'RGBA'):
        image = image.convert('RGB')

    # get size
    thumb_w, thumb_h = thumb_size
    # If you want to generate a square thumbnail
    if thumb_w == thumb_h:
        # quad
        xsize, ysize = image.size
        # get minimum size
        minsize = min(xsize,ysize)
        # largest square possible in the image
        xnewsize = (xsize-minsize)/2
        ynewsize = (ysize-minsize)/2
        # crop it
        image2 = image.crop((xnewsize, ynewsize, xsize-xnewsize, ysize-ynewsize))
        # load is necessary after crop
        image2.load()
        # thumbnail of the cropped image (with ANTIALIAS to make it look better)
        image2.thumbnail(thumb_size, Image.ANTIALIAS)
    else:
        # not quad
        image2 = image
        image2.thumbnail(thumb_size, Image.ANTIALIAS)

    io = cStringIO.StringIO()
    # PNG and GIF are the same, JPG is JPEG
    if format.upper()=='JPG':
        format = 'JPEG'

    image2.save(io, format)
    return ContentFile(io.getvalue())

class ImageWithThumbsFieldFile(ImageFieldFile):
    """
    See ImageWithThumbsField for usage example
    """
    def __init__(self, *args, **kwargs):
        super(ImageWithThumbsFieldFile, self).__init__(*args, **kwargs)

        if self.field.sizes:
            def get_size(self, size):
                if not self:
                    return ''
                else:
                    split = self.url.rsplit('.',1)
                    thumb_url = '%s.%sx%s.%s' % (split[0],w,h,split[1])
                    return thumb_url

            for size in self.field.sizes:
                (w,h) = size
                setattr(self, 'url_%sx%s' % (w,h), get_size(self, size))

    def save(self, name, content, save=True):
        super(ImageWithThumbsFieldFile, self).save(name, content, save)

        if self.field.sizes:
            for size in self.field.sizes:
                (w,h) = size
                split = self.name.rsplit('.',1)
                thumb_name = '%s.%sx%s.%s' % (split[0],w,h,split[1])

                # you can use another thumbnailing function if you like
                thumb_content = generate_thumb(content, size, split[1])

                thumb_name_ = self.storage.save(thumb_name, thumb_content)

                if not thumb_name == thumb_name_:
                    raise ValueError('There is already a file named %s' % thumb_name)

    def delete(self, save=True):
        name=self.name
        super(ImageWithThumbsFieldFile, self).delete(save)
        if self.field.sizes:
            for size in self.field.sizes:
                (w,h) = size
                split = name.rsplit('.',1)
                thumb_name = '%s.%sx%s.%s' % (split[0],w,h,split[1])
                try:
                    self.storage.delete(thumb_name)
                except:
                    pass

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
#=================================================================================================================================================================================

class Photo(models.Model):
    from django.contrib.contenttypes.models import ContentType
    content_type = models.ForeignKey(ContentType, related_name='related_Photo', )
    object_id = models.PositiveIntegerField(db_index=True, )
    from django.contrib.contenttypes import generic
    parent = generic.GenericForeignKey('content_type', 'object_id', )
    main = models.NullBooleanField(verbose_name=u'Признак главной фотографии',
        null=False, blank=False, default=False, )
    def set_path_photo(self, filename):
        return 'photo/%.6d/%s' % (
#            self.product.pub_datetime.year,
            self.object_id,
            filename)
#    from compat.ImageWithThumbs.thumbs import ImageWithThumbsField
    photo = ImageWithThumbsField(verbose_name=u'Фото', upload_to=set_path_photo, sizes=((90,95),(205,190),(345,370),(700,500),),
                                 blank=False, null=False, )
    title = models.CharField(verbose_name=u'Заголовок фотографии', max_length=256,
        null=False, blank=False, )
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
    meta_title = models.CharField(verbose_name=u'title фотографии', max_length=190,
        null=True, blank=True,
                                   help_text=u'Данный title читают поисковые системы для правильного расположения фотографии в поиске.', )
    meta_alt = models.CharField(verbose_name=u'alt фотографии', max_length=190,
        null=True, blank=True,
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
