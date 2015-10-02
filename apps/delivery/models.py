# -*- coding: utf-8 -*-
__author__ = 'Alex Starov'

from django.db import models
from django.utils.translation import ugettext_lazy as _

from datetime import date, datetime


class MailAccount(models.Model, ):
    email = models.CharField(verbose_name=_(u'E-Mail', ),
                             max_length=64,
                             blank=False,
                             null=False, )
    smtp_server = models.CharField(verbose_name=_(u'SMTP Server', ),
                                   max_length=64,
                                   blank=False,
                                   null=False, )
    smtp_port = models.PositiveSmallIntegerField(verbose_name=_(u'SMTP Port', ),
                                                 blank=True,
                                                 null=True,
                                                 default=25, )
    login = models.CharField(verbose_name=_(u'UserName - login', ),
                             max_length=64,
                             blank=False,
                             null=False, )
    password = models.CharField(verbose_name=_(u'User password', ),
                                max_length=64,
                                blank=False,
                                null=False, )
    use_tls = models.BooleanField(verbose_name=_(u'Use TLS', ),
                                  default=True, )
    #Дата создания и дата обновления. Устанавливаются автоматически.
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name=_(u'Дата создания', ),
                                      blank=True,
                                      null=True,
                                      default=datetime.now(), )
    updated_at = models.DateTimeField(auto_now=True,
                                      verbose_name=_(u'Дата обновления', ),
                                      blank=True,
                                      null=True,
                                      default=datetime.now(), )

    def __unicode__(self):
        return u'%s -> %s:%d -> Login: %s' % (self.email, self.smtp_server, self.smtp_port, self.login, )

    class Meta:
        db_table = 'MailAccount'
        ordering = ['-created_at', ]
        verbose_name = u'SMTP Account'
        verbose_name_plural = u'SMTP Accounts'


class Delivery(models.Model, ):
    name = models.CharField(verbose_name=_(u'Имя рассылки', ),
                            max_length=128,
                            blank=True,
                            null=True,
                            default=datetime.now().isoformat(), )
    Type_Mailings = (
        (1, _(u'Акция', ), ),
        # (2, _(u'Под заказ', ), ),
        # (3, _(u'Ожидается', ), ),
        # (4, _(u'Недоступен', ), ),
    )
    delivery_test = models.BooleanField(verbose_name=_(u'Тестовая рассылка', ),
                                        blank=True,
                                        null=False,
                                        default=True, )
    send_test = models.BooleanField(verbose_name=_(u'Тестовая рассылка отослана', ),
                                    blank=True,
                                    null=False,
                                    default=True, )
    send_general = models.BooleanField(verbose_name=_(u'Главная рассылка отослана', ),
                                       blank=True,
                                       null=False,
                                       default=True, )
    type = models.PositiveSmallIntegerField(verbose_name=_(u'Тип рассылки'),
                                            choices=Type_Mailings,
                                            default=1,
                                            blank=False,
                                            null=False, )
    subject = models.CharField(verbose_name=_(u'Subject рассылки', ),
                               max_length=256,
                               blank=True,
                               null=True, )
    html = models.TextField(verbose_name=_(u'Html текст рассылки "СЫРОЙ"', ),
                            blank=True,
                            null=True, )
    real_html = models.TextField(verbose_name=_(u'Html текст рассылки', ),
                                 blank=True,
                                 null=True, )
    #Дата создания и дата обновления. Устанавливаются автоматически.
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name=_(u'Дата создания', ),
                                      blank=True,
                                      null=True,
                                      default=datetime.now(), )
    updated_at = models.DateTimeField(auto_now=True,
                                      verbose_name=_(u'Дата обновления', ),
                                      blank=True,
                                      null=True,
                                      default=datetime.now(), )

    from django.contrib.contenttypes import generic
    from apps.utils.mediafile.models import MediaFile
    img = generic.GenericRelation(MediaFile,
                                  content_type_field='content_type',
                                  object_id_field='object_id', )

    def save(self, *args, **kwargs):
        real_html = self.html
        def_str1 = u'<figure><p><img src='
        def_str2 = u'</figure>'
        while def_str1 in real_html:
            try:
                val_begin = real_html.index(def_str1)
            except ValueError:
                break
            else:
                pass
            try:
                val_end = real_html.index(def_str2)
            except ValueError:
                break
            else:
                val_end += 9
            real_html = u'%s%s' % (real_html[:val_begin], real_html[val_end:], )
        img = self.img.all()
        if img.count() > 0:
            for i in range(1, img.count()+1, ):
                def_str = u'{{ фото:%.1d }}' % i
                if def_str in real_html:
                    img_aaa = img[i-1].img
                    #old_name = img[i-1].img.name
                    thumb_size = ((img[i-1].height, img[i-1].width, ), )
                    #file_name = img_aaa.name.rsplit('/', 1, )[1]
                    #file_format = file_name.rsplit('.', 1, )[1]
                    from compat.ImageWithThumbs.utils import generate_thumb
                    img_aaa.field.sizes = thumb_size
                    #img_aaa.save(name=file_name,
                    #             content=generate_thumb(img=img_aaa,
                    #                                    thumb_size=thumb_size[0],
                    #                                    format=file_format, ), )
                    #img_url = 'img_aaa.url_%dx%d' % (img[i-1].height, img[i-1].width, )
                    #img_url = eval(img_url,
                    #               {'__builtins__': {}, },
                    #               {'img_aaa': img_aaa, }, )
                    img_url = img_aaa.url.rsplit('.', 1, )
                    img_url = '%s_%dx%d.%s' % (img_url[0], img[i-1].height, img[i-1].width, img_url[1], )
                    from django.template.loader import render_to_string
                    link_str = render_to_string('render_img_string.jinja2.html',
                                                {'imgN': def_str,
                                                 'img_url': img_url,
                                                 'alt': img[i-1].meta_alt,
                                                 'title': img[i-1].title,
                                                 'caption': img[i-1].sign, }, )
                    #value = eval(string,
                    #     {'__builtins__': {}, },
                    #     {'variable_set': variable_set, }, )
                    real_html = real_html.replace(def_str, link_str, )
                    #try:
                    #    img_aaa.storage.delete(old_name, )
                    #except:
                    #    pass

        self.real_html = real_html
        super(Delivery, self).save(*args, **kwargs)  # Call the "real" save() method.

    @property
    def text_type(self):
        return self.Type_Mailings[self.type-1][1]

    @property
    def get_url_number(self):
        return '%06d' % self.id

    @models.permalink
    def get_absolute_url(self, ):
        return ('admin_delivery:edit',
                (),
                {'delivery_id': self.get_url_number, }, )
#                {'delivery_id': '%06d' % self.pk, }, )

    def __unicode__(self):
        # """
        # Проверка DocTest
        # >>> category = Category.objects.create(title=u'Proverka123  -ф123')
        # >>> category.item_description = u'Тоже проверка'
        # >>> category.save()
        # >>> if type(category.__unicode__()) is unicode:
        # ...     print category.__unicode__() #.encode('utf-8')
        # ... else:
        # ...     print type(category.__unicode__())
        # ...
        # Категория: Proverka123  -ф123
        # >>> print category.title
        # Proverka123  -ф123
        # """
        return u'Рассылка: № %6d - %s' % (self.pk, self.name, )

#    def save(self, *args, **kwargs):
#        from django.utils.timezone import now
#        if not self.created_at:
#            self.created_at = now()
#        self.updated_at = now()
#        return super(CouponGroup, self).save(*args, **kwargs)

    class Meta:
        db_table = 'Delivery'
        ordering = ['-created_at', ]
        verbose_name = u'Рассылка'
        verbose_name_plural = u'Рассылки'


class EmailMiddleDelivery(models.Model, ):
    delivery = models.ForeignKey(to=Delivery,
                                 verbose_name=_(u'Указатель на рассылку', ),
                                 blank=False,
                                 null=False, )
    delivery_test_send = models.BooleanField(verbose_name=_(u'Тестовая рассылка - отослана', ),
                                             blank=True,
                                             null=False,
                                             default=True, )
    delivery_send = models.BooleanField(verbose_name=_(u'Рассылка - отослана', ),
                                        blank=True,
                                        null=False,
                                        default=True, )
    #Дата создания и дата обновления. Устанавливаются автоматически.
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name=_(u'Дата создания', ),
                                      blank=True,
                                      null=True,
                                      default=datetime.now(), )
    updated_at = models.DateTimeField(auto_now=True,
                                      verbose_name=_(u'Дата обновления', ),
                                      blank=True,
                                      null=True,
                                      default=datetime.now(), )

    def __unicode__(self):
        return u'Промежуток рассылки: № %6d - %s, Test: %s, Send: %s, created_at: %s, updated_at: %s'\
               % (self.pk, self.delivery.name, self.delivery_test_send, self.delivery_send,
                  self.created_at, self.updated_at, )

    class Meta:
        db_table = 'EmailMiddleDelivery'
        ordering = ['-created_at', ]
        verbose_name = u'Промежуточная можель Рассылки'
        verbose_name_plural = u'Промежуточные можели Рассылок'


class EmailForDelivery(models.Model, ):
    delivery = models.ForeignKey(to=EmailMiddleDelivery,
                                 verbose_name=_(u'Указатель на рассылку', ),
                                 blank=False,
                                 null=False, )
    from apps.authModel.models import Email
    email = models.ForeignKey(to=Email,
                              verbose_name=_(u'E-Mail', ),
                              blank=False,
                              null=False, )
    send = models.BooleanField(verbose_name=_(u'Флаг отсылки', ),
                               blank=True,
                               null=False,
                               default=False, )
    #Дата создания и дата обновления. Устанавливаются автоматически.
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name=_(u'Дата создания', ),
                                      blank=True,
                                      null=True,
                                      default=datetime.now(), )
    updated_at = models.DateTimeField(auto_now=True,
                                      verbose_name=_(u'Дата обновления', ),
                                      blank=True,
                                      null=True,
                                      default=datetime.now(), )

    class Meta:
        db_table = 'EmailForDelivery'
        ordering = ['-created_at', ]
        verbose_name = u'Модель Рассылки (Email адрес)'
        verbose_name_plural = u'Модели Рассылок (Email адреса)'
