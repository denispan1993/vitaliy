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
    category = models.ManyToManyField(Category, verbose_name=u'Категории',
        related_name=u'products', null=False, blank=False, )
    url = models.SlugField(verbose_name=u'URL адрес продукта', max_length=128,
        null=False, blank=False, )
    title = models.CharField(verbose_name=u'Заголовок продукта', max_length=256,
        null=False, blank=False, )
    name = models.CharField(verbose_name=u'Наименование продукта', max_length=256,
        null=True, blank=True, )
    description = models.TextField(verbose_name=u'Описание продукта',
        null=True, blank=True, )

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

#    def get_absolute_url(self, ):
#        return '/news/rubric/%s/' % self.url

    def __unicode__(self):
        return u'Продукт:%s' % (self.title, )

    class Meta:
        db_table = 'Product'
        ordering = ['-created_at']
        verbose_name = u'Продукт'
        verbose_name_plural = u'Продукты'

class Photo(models.Model):
    from django.contrib.contenttypes.models import ContentType
    content_type = models.ForeignKey(ContentType, related_name='related_Photo', )
    object_id = models.PositiveIntegerField(db_index=True, )
    from django.contrib.contenttypes import generic
    parent = generic.GenericForeignKey('content_type', 'object_id', )
    main = models.NullBooleanField(verbose_name=u'Признак главной фотографии',
        null=False, blank=False, default=False, )
    title = models.CharField(verbose_name=u'Заголовок фотографии', max_length=256,
        null=False, blank=False, )
    name = models.CharField(verbose_name=u'Наименование фотографии', max_length=256,
        null=True, blank=True, )
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
