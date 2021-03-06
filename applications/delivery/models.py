# -*- coding: utf-8 -*-
# /applications/delivery/models.py

import string
import random
from datetime import datetime
from django.db import models, IntegrityError
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.template.loader import render_to_string

from compat.ImageWithThumbs import models as class_ImageWithThumb
from applications.cart.models import Order
from applications.authModel.models import Email as authModel_Email

from applications.utils.captcha.utils import key_generator
__author__ = 'AlexStarov'


def hash_8(size=8, ):
    return key_generator(size=size, )


def hash_16(size=16, ):
    return key_generator(size=size, )


def hash_64(size=64, ):
    return key_generator(size=size, )


class MailServer(models.Model, ):
    server_name = models.CharField(verbose_name=_(u'Server Name', ),
                                   max_length=64,
                                   blank=True,
                                   null=True, )
    use_smtp = models.BooleanField(verbose_name=_(u'Сервер активный', ),
                                   blank=False,
                                   null=False,
                                   default=True, )

    server_smtp = models.CharField(verbose_name=_(u'SMTP Server', ),
                                   max_length=128,
                                   blank=True,
                                   null=True, )

    port_smtp = models.PositiveSmallIntegerField(verbose_name=_(u'SMTP Port', ),
                                                 blank=True,
                                                 null=True,
                                                 default=465, )
    use_tls_smtp = models.BooleanField(verbose_name=_(u'SMTP Use TLS', ),
                                       default=True, )
    use_ssl_smtp = models.BooleanField(verbose_name=_(u'SMTP Use SSL', ),
                                       default=False, )

    use_imap = models.BooleanField(verbose_name=_(u'Use IMAP protocol', ),
                                   default=False, )
    server_imap = models.CharField(verbose_name=_(u'IMAP Server', ),
                                   max_length=128,
                                   blank=True,
                                   null=True, )
    port_imap = models.PositiveSmallIntegerField(verbose_name=_(u'IMAP Port', ),
                                                 blank=True,
                                                 null=True,
                                                 default=993, )
    use_tls_imap = models.BooleanField(verbose_name=_(u'IMAP Use TLS', ),
                                       default=True, )
    use_ssl_imap = models.BooleanField(verbose_name=_(u'IMAP Use SSL', ),
                                       default=False, )

    use_pop3 = models.BooleanField(verbose_name=_(u'Use POP3 protocol', ),
                                   default=False, )
    server_pop3 = models.CharField(verbose_name=_(u'POP3 Server', ),
                                   max_length=128,
                                   blank=True,
                                   null=True, )
    port_pop3 = models.PositiveSmallIntegerField(verbose_name=_(u'POP3 Port', ),
                                                 blank=True,
                                                 null=True,
                                                 default=995, )
    use_tls_pop3 = models.BooleanField(verbose_name=_(u'POP3 Use TLS', ),
                                       default=True, )
    use_ssl_pop3 = models.BooleanField(verbose_name=_(u'POP3 Use SSL', ),
                                       default=False, )

    #Дата создания и дата обновления. Устанавливаются автоматически.
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name=_(u'Дата создания', ),
                                      blank=True,
                                      null=True, )
                                      # default=datetime.now(), )
    updated_at = models.DateTimeField(auto_now=True,
                                      verbose_name=_(u'Дата обновления', ),
                                      blank=True,
                                      null=True, )
                                      # default=datetime.now(), )

    def __str__(self):
        return u'%s:%d' % (self.server_smtp, self.port_smtp, )

    class Meta:
        db_table = 'Delivery_MailServer'
        ordering = ['-created_at', ]
        verbose_name = u'Mail Server'
        verbose_name_plural = u'Mail Servers'


class MailAccount(models.Model, ):
    use_smtp = models.BooleanField(verbose_name=_(u'Аккаунт активный', ),
                                    blank=False,
                                    null=False,
                                    default=True, )

    is_auto_active = models.BooleanField(verbose_name=_(u'Аккаунт автоматически активный', ),
                                         blank=False,
                                         null=False,
                                         default=True, )
    auto_active_datetime = models.DateTimeField(verbose_name=_(u'Дата закрытия аккаунта',),
                                                blank=False,
                                                null=False,
                                                default=datetime.now, )

    email = models.CharField(verbose_name=_(u'E-Mail', ),
                             max_length=64,
                             blank=False,
                             null=False, )
    username = models.CharField(verbose_name=_(u'UserName - login', ),
                                max_length=64,
                                blank=False,
                                null=False, )
    password = models.CharField(verbose_name=_(u'User password', ),
                                max_length=64,
                                blank=False,
                                null=False, )

    use_imap = models.BooleanField(verbose_name=_(u'Use IMAP protocol', ),
                                   default=False, )

    use_pop3 = models.BooleanField(verbose_name=_(u'Use POP3 protocol', ),
                                   default=False, )

    server = models.ForeignKey(verbose_name=_(u'Server', ),
                               to='MailServer',
                               blank=False,
                               null=False, )

    #Дата создания и дата обновления. Устанавливаются автоматически.
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name=_(u'Дата создания', ),
                                      blank=True,
                                      null=True, )
                                      # default=datetime.now(), )
    updated_at = models.DateTimeField(auto_now=True,
                                      verbose_name=_(u'Дата обновления', ),
                                      blank=True,
                                      null=True, )
                                      #default=datetime.now(), )

    @property
    def get_provider(self):
        return self.email.split('@')[1]

    @property
    def get_return_path_subscribe(self):
        return 'subscribe@{0}'.format(self.get_provider, )

    # @property
    # def is_active(self):
    #     return self.server.is_active

    def __str__(self):
        return u'%s --> %s:%d' % (self.email, self.server.server_smtp, self.server.port_smtp, )

    class Meta:
        db_table = 'Delivery_MailAccount'
        ordering = ['-created_at', ]
        get_latest_by = 'pk'
        verbose_name = _(u'Mail Account', )
        verbose_name_plural = _(u'Mail Accounts', )


def datetime_in_iso_format():
    return datetime.now().isoformat()


class Delivery(models.Model, ):
    name = models.CharField(verbose_name=_(u'Имя рассылки', ),
                            max_length=128,
                            blank=True,
                            null=True,
                            default=datetime_in_iso_format, )
    Type_Mailings = (
        (1, _(u'Фэйк рассылка', ), ),
        (2, _(u'Акция', ), ),
        (3, _(u'Новинки', ), ),
        (4, _(u'Рассылка на "SPAM" адреса', ), ),
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
    send_spam = models.BooleanField(verbose_name=_(u'SPAM рассылка отослана', ),
                                    blank=True,
                                    null=False,
                                    default=False, )
    send_general = models.BooleanField(verbose_name=_(u'Главная рассылка отослана', ),
                                       blank=True,
                                       null=False,
                                       default=True, )
    type = models.PositiveSmallIntegerField(verbose_name=_(u'Тип рассылки'),
                                            choices=Type_Mailings,
                                            default=1,
                                            blank=False,
                                            null=False, )

    # subject = models.CharField(verbose_name=_(u'Subject рассылки', ),
    #                            max_length=256,
    #                            blank=True,
    #                            null=True, )

    #html = models.TextField(verbose_name=_(u'Html текст рассылки "СЫРОЙ"', ),
    #                        blank=True,
    #                        null=True, )
    #real_html = models.TextField(verbose_name=_(u'Html текст рассылки', ),
    #                             blank=True,
    #                             null=True, )
    #Дата создания и дата обновления. Устанавливаются автоматически.
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name=_(u'Дата создания', ),
                                      blank=True,
                                      null=True, )
    updated_at = models.DateTimeField(auto_now=True,
                                      verbose_name=_(u'Дата обновления', ),
                                      blank=True,
                                      null=True, )

    # Вспомогательные поля
    img = GenericRelation(
        to='Email_Img',
        content_type_field='content_type',
        object_id_field='object_id', )

    """ def save(self, *args, **kwargs):
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
                    link_str = render_to_string('render_img_string.jinja2',
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
        super(Delivery, self).save(*args, **kwargs)  # Call the "real" save() method."""

    @property
    def emails_delivered(self):
        EmailMiddleDelivery_all = EmailMiddleDelivery.objects.filter(delivery=self,
                                                                     delivery_test_send=False,
                                                                     spam_send=False,
                                                                     delivery_send=True, ).values_list('pk', flat=True, )
        if len(EmailMiddleDelivery_all, ) < 1:
            EmailMiddleDelivery_all = EmailMiddleDelivery.objects.filter(delivery=self,
                                                                         delivery_test_send=False,
                                                                         spam_send=True,
                                                                         delivery_send=False, ).values_list('pk', flat=True, )
        i = 0
        if not EmailMiddleDelivery_all == []:
            i += EmailForDelivery.objects.filter(delivery_id__in=EmailMiddleDelivery_all, ).count()
        return i

    @property
    def trace_of_visits(self):
        return TraceOfVisits.objects.filter(delivery=self, )\
            .exclude(email__delivery__delivery_test_send=True, )\
            .count()

    @property
    def trace_of_visits_unique(self):
        return TraceOfVisits.objects.filter(delivery=self, )\
            .exclude(email__delivery__delivery_test_send=True, )\
            .values('email__content_type', 'email__object_id', )\
            .distinct()\
            .count()

    @property
    def order_from_trace_of_visits(self):
        trace_of_visits = TraceOfVisits.objects.filter(delivery=self, )\
            .exclude(email__delivery__delivery_test_send=True, )
        # unique_trace_email_pk = set()
        unique_trace_pks = set([trace.email.now_email.pk for trace in trace_of_visits])
        # print unique_trace_pks
        unique_trace_emails = set([trace.email.now_email.email for trace in trace_of_visits])
        # print unique_trace_emails
        # for trace in trace_of_visits:
        #     trace_email_pk = trace.email.now_email.pk
        #     if trace_email_pk not in unique_trace_email_pk:
        #         unique_trace_email_pk.append(trace_email_pk, )
        #from datetime import timedelta
        #delta = timedelta(days=100, )
        unique_orders = []
        # for trace_pk in unique_trace_email_pk:
        #     try:
        #         this_trace = trace_of_visits.get(pk__in=trace_pk, )
        #     except TraceOfVisits.DoesNotExist:
        #         continue
        #     else:

        q = Q()
        for email in unique_trace_emails:
            q |= Q(email__icontains=email)

        try:
            orders = Order.objects.filter(q, ).values('email').distinct()  # email__icontains=unique_trace_emails, )  # this_trace.email.now_email.email, )
                                      # created_at__lte=this_trace.cteated_at + delta, )
        except Order.DoesNotExist:
            return 0
        # except Order.MultipleObjectsReturned:
        #     unique_orders.append(1, )
        # else:
        #     unique_orders.append(order.pk, )

        # return len(unique_orders, )

        return len(orders, )

    @property
    def emails(self):
        return authModel_Email.objects.count()

    @property
    def subjects(self):
        return self.subject_set.all().order_by('pk', )

    @property
    def bodies(self):
        return self.body_set.all().order_by('pk', )

    @property
    def urls(self):
        return self.url_set.all().order_by('pk', )

    @property
    def images(self):
        return self.img.all().order_by('pk', )

    @property
    def bad_emails(self):
        return authModel_Email.objects.filter(bad_email=True, ).count()

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

    def __str__(self):
        # """
        # Проверка DocTest
        # >>> category = Category.objects.create(title=u'Proverka123  -ф123')
        # >>> category.item_description = u'Тоже проверка'
        # >>> category.save()
        # >>> if type(category.__str__()) is unicode:
        # ...     print category.__str__() #.encode('utf-8')
        # ... else:
        # ...     print type(category.__str__())
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
        db_table = 'Delivery_Delivery'
        ordering = ['-created_at', ]
        verbose_name = u'Рассылка'
        verbose_name_plural = u'Рассылки'


class Subject(models.Model, ):
    delivery = models.ForeignKey(to=Delivery,
                                 blank=False,
                                 null=False,)

    subject = models.CharField(verbose_name=_(u'Тема письма', ),
                               max_length=256,
                               blank=False,
                               null=False,
                               default=_(u'Тема', ), )

    chance = models.DecimalField(verbose_name=_(u'Вероятность', ),
                                 max_digits=4,
                                 decimal_places=2,
                                 blank=False,
                                 null=False,
                                 default=1, )
    #Дата создания и дата обновления. Устанавливаются автоматически.
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name=_(u'Дата создания', ),
                                      blank=True,
                                      null=True, )
    updated_at = models.DateTimeField(auto_now=True,
                                      verbose_name=_(u'Дата обновления', ),
                                      blank=True,
                                      null=True, )

    def __str__(self):
        return u'Тема: № %6d --> [%s]:%2.2f' % (self.pk, self.subject, self.chance )

    class Meta:
        db_table = 'Delivery_Subject'
        ordering = ['-created_at', ]
        verbose_name = _(u'Тема', )
        verbose_name_plural = _(u'Темы', )


class Body(models.Model, ):
    delivery = models.ForeignKey(to=Delivery,
                                 blank=False,
                                 null=False, )

    html = models.TextField(verbose_name=_(u'Тело письма', ),
                            blank=False,
                            null=False,
                            default=_(u'<html><head></head><body></body></html>', ), )

    real_html = models.TextField(verbose_name=_(u'Тело письма', ),
                                 blank=False,
                                 null=False,
                                 default=_(u'<html><head></head><body></body></html>', ), )

    text = models.TextField(verbose_name=_(u'Тело письма', ),
                            blank=False,
                            null=False,
                            default=_(u'', ), )

    chance = models.DecimalField(verbose_name=_(u'Вероятность', ),
                                 max_digits=4,
                                 decimal_places=2,
                                 blank=False,
                                 null=False,
                                 default=1, )
    #Дата создания и дата обновления. Устанавливаются автоматически.
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name=_(u'Дата создания', ),
                                      blank=True,
                                      null=True, )
    updated_at = models.DateTimeField(auto_now=True,
                                      verbose_name=_(u'Дата обновления', ),
                                      blank=True,
                                      null=True, )

    def __str__(self):
        return u'Тело письма: № %6d --> %s.... (%2.2f)' % (self.pk, self.html[0:50], self.chance)

    class Meta:
        db_table = 'Delivery_Body'
        ordering = ['-created_at', ]
        verbose_name = _(u'Тело письма', )
        verbose_name_plural = _(u'Тема писем', )


class Url(models.Model, ):
    delivery = models.ForeignKey(to=Delivery,
                                 verbose_name=_(u'Рассылка'),
                                 blank=False,
                                 null=False,)

    url_id = models.PositiveSmallIntegerField(verbose_name=_(u'Url ID'),
                                              blank=True,
                                              null=True, )

    href = models.CharField(verbose_name=_(u'URL', ),
                            max_length=256,
                            blank=False,
                            null=False,
                            default='http://keksik.com.ua/', )

    anchor = models.CharField(verbose_name=_(u'Якорь --> "Анкор"', ),
                              max_length=256,
                              blank=True,
                              null=True, )

    title = models.CharField(verbose_name=_(u'Title', ),
                             max_length=256,
                             blank=True,
                             null=True, )
    Type_Url = (
        (1, _(u'Url', ), ),
        (2, _(u'Unsub', ), ),
        (3, _(u'Open', ), ),
    )
    type = models.PositiveSmallIntegerField(verbose_name=_(u'Тип URL'),
                                            choices=Type_Url,
                                            default=1,
                                            blank=False,
                                            null=False, )


    #Дата создания и дата обновления. Устанавливаются автоматически.
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name=_(u'Дата создания', ),
                                      blank=True,
                                      null=True, )
    updated_at = models.DateTimeField(auto_now=True,
                                      verbose_name=_(u'Дата обновления', ),
                                      blank=True,
                                      null=True, )

    def __str__(self):
        if self.type == 1:
            return u'pk:%0.6d [url%d] --> %s:%s' % (
                self.pk,
                self.url_id,
                self.anchor,
                self.title, )
        elif self.type == 2:
            return u'pk:%0.6d [unsub] --> %s' % (
                self.pk,
                self.href, )
        elif self.type == 3:
            return u'pk:%0.6d [open] --> %s' % (
                self.pk,
                self.href, )

    class Meta:
        db_table = 'Delivery_Url'
        ordering = ['-created_at', ]
        verbose_name = _(u'Url', )
        verbose_name_plural = _(u'Urls', )


def set_path_photo(self, filename):
    return 'email_img/%.6d/%s' % (
        # self.product.pub_datetime.year,
        self.object_id,
        filename)


def set_path_img(self, filename):
    return 'email_img/%.6d/%s' % (
        # self.product.pub_datetime.year,
        self.object_id,
        filename)


class Email_Img(models.Model):
    content_type = models.ForeignKey(ContentType, related_name='related_Email_Img', )
    object_id = models.PositiveIntegerField(db_index=True, )
    parent = GenericForeignKey('content_type', 'object_id', )

    name = models.CharField(verbose_name=_(u'Наименование картинки', ),
                            max_length=256,
                            null=True,
                            blank=True, )

    tag_name = models.CharField(verbose_name=_(u"Имя tag'a картинки", ),
                                max_length=8,
                                null=True,
                                blank=True,
                                help_text=_(u'TAG картинки не может быть длинее 8 символов,'
                                            u' только английские маленькие буквы и цифры'
                                            u' без пробелов и подчеркиваний', ), )

    image = class_ImageWithThumb.ImageWithThumbsField(verbose_name=u'Картинка',
                                                      upload_to=set_path_img,
                                                      sizes=((26, 26, ), (50, 50, ), (90, 95, ),
                                                             (205, 190, ), (210, 160, ), (345, 370, ),
                                                             (700, 500, ), ),
                                                      blank=False,
                                                      null=False, )
    #Дата создания и дата обновления новости. Устанавливаются автоматически.
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True, )

    def __str__(self):
        return u'Картинка для E-Mail: %s' % (self.name, )

    class Meta:
        db_table = 'EMail_Img'
        ordering = ['-created_at', ]
        verbose_name = "Картинка для E-Mail"
        verbose_name_plural = "Картинкии для E-Mail"


class EmailMiddleDelivery(models.Model, ):
    delivery = models.ForeignKey(to=Delivery,
                                 verbose_name=_(u'Указатель на рассылку', ),
                                 blank=False,
                                 null=False, )
    delivery_test_send = models.BooleanField(verbose_name=_(u'Тестовая рассылка - отослана', ),
                                             blank=True,
                                             null=False,
                                             default=True, )
    spam_send = models.BooleanField(verbose_name=_(u'SPAM рассылка - отослана', ),
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
                                      null=True, )
                                      # default=datetime.now(), )
    updated_at = models.DateTimeField(auto_now=True,
                                      verbose_name=_(u'Дата обновления', ),
                                      blank=True,
                                      null=True, )
                                      # default=datetime.now(), )

    def __str__(self):
        return u'Промежуток рассылки: № %6d - %s, Test: %s, Send: %s, created_at: %s, updated_at: %s'\
               % (self.pk, self.delivery.name, self.delivery_test_send, self.delivery_send,
                  self.created_at, self.updated_at, )

    class Meta:
        db_table = 'Delivery_EmailMiddleDelivery'
        ordering = ['-created_at', ]
        verbose_name = u'Промежуточная модель Рассылки'
        verbose_name_plural = u'Промежуточные модели Рассылок'


class EmailForDelivery(models.Model, ):
    delivery = models.ForeignKey(to=EmailMiddleDelivery,
                                 verbose_name=_(u'Указатель на рассылку', ),
                                 blank=False,
                                 null=False, )
    key = models.CharField(verbose_name=_(u'ID E-Mail адреса и рассылки', ),
                           max_length=8,
                           blank=False,
                           null=False,
                           # unique=True, )
                           default=hash_8, )
    email = models.ForeignKey(to=authModel_Email,
                              verbose_name=_(u'E-Mail', ),
                              blank=True,
                              null=True, )
    content_type = models.ForeignKey(ContentType,
                                     related_name='email_instance',
                                     verbose_name=_(u'Указатель на E-Mail', ),
                                     blank=True,
                                     null=True, )
    object_id = models.PositiveIntegerField(db_index=True,
                                            blank=True,
                                            null=True, )
    now_email = GenericForeignKey('content_type', 'object_id', )

    send = models.BooleanField(verbose_name=_(u'Флаг отсылки', ),
                               blank=True,
                               null=False,
                               default=False, )
    #Дата создания и дата обновления. Устанавливаются автоматически.
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name=_(u'Дата создания', ),
                                      blank=True,
                                      null=True, )
    updated_at = models.DateTimeField(auto_now=True,
                                      verbose_name=_(u'Дата обновления', ),
                                      blank=True,
                                      null=True, )

    def save(self, *args, **kwargs):
        if not self.pk:
            while True:
                key = key()
                try:
                    EmailForDelivery.objects.get(key=key, )
                except EmailForDelivery.DoesNotExist:
                    self.key = key
                    break
                except IntegrityError:
                    print('IntegrityError Key: %s' % key, )
                except Exception as e:
                    print('Exception type: %s, message: %s' % (type(e, ), e, ), )
        super(EmailForDelivery, self).save(*args, **kwargs)

    def __str__(self):
        return u'E-Mail: %s pk: %6d created_at: %s, updated_at: %s'\
               % (self.now_email.email, self.pk, self.created_at, self.updated_at, )

    class Meta:
        db_table = 'Delivery_EmailForDelivery'
        ordering = ['-created_at', ]
        verbose_name = u'Рассылка (Email адрес)'
        verbose_name_plural = u'Рассылки (Email адреса)'


class TraceOfVisits(models.Model, ):
    delivery = models.ForeignKey(to=Delivery,
                                 verbose_name=_(u'Указатель на рассылку', ),
                                 blank=False,
                                 null=False, )
    email = models.ForeignKey(to=EmailForDelivery,
                              verbose_name=_(u'Указатель на E-Mail пользователя', ),
                              blank=True,
                              null=True, )
    sessionid = models.CharField(verbose_name=u'SessionID',
                                 max_length=32,
                                 blank=True,
                                 null=True,
                                 default=0, )
    url = models.CharField(verbose_name=_(u'URL переадресации', ),
                           max_length=255,
                           blank=True,
                           null=True, )

    Type_Url = (
        (1, _(u'Url', ), ),
        (2, _(u'Unsub', ), ),
        (3, _(u'Open', ), ),
    )
    type = models.PositiveSmallIntegerField(verbose_name=_(u'Тип URL'),
                                            choices=Type_Url,
                                            default=1,
                                            blank=False,
                                            null=False, )

    target = models.CharField(verbose_name=_(u'Цэль захода на сайт'),
                              max_length=32,
                              blank=True,
                              null=True, )
    target_id = models.PositiveSmallIntegerField(verbose_name=_(u'Тип цэли обращения к сайту'),
                                                 blank=True,
                                                 null=True, )

    content_type = models.ForeignKey(ContentType,
                                     verbose_name=_(u'Указатель на E-Mail', ),
                                     blank=True,
                                     null=True, )
    object_id = models.PositiveIntegerField(db_index=True,
                                            blank=True,
                                            null=True, )
    now_email = GenericForeignKey('content_type', 'object_id', )

    #Дата создания и дата обновления. Устанавливаются автоматически.
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name=_(u'Дата создания', ),
                                      blank=True,
                                      null=True, )
                                      # default=datetime.now(), )

    @property
    def delivery_fk(self):
        return self.delivery.name

    @property
    def email_fk(self):
        if self.email.now_email:
            return self.email.now_email.email
        if self.email:
            return self.email.now_email

    @property
    def email_fk_key(self):
        return self.email.key

    class Meta:
        db_table = 'Delivery_TraceOfVisits'
        ordering = ['-created_at', ]
        verbose_name = u'След от посещения'
        verbose_name_plural = u'Следы от посещений'


class SpamEmail(models.Model, ):
    email = models.EmailField(verbose_name=_(u'E-Mail', ),
                              blank=False,
                              null=False, )
    hash = models.CharField(verbose_name=u'Hash',
                            unique=False,
                            max_length=16,
                            default=hash_16,
                            blank=False,
                            null=False, )

    # Тест e'mail
    test = models.BooleanField(
        verbose_name=_(u"Тест e'mail", ),
        default=False, )
    # Рассылка Спам
    delivery_spam = models.BooleanField(verbose_name=_(u'Спам', ),
                                        default=True, )
    # Рассылка новых продуктов
    delivery_new_products = models.BooleanField(verbose_name=_(u'Новые продукты', ),
                                                default=True, )
    # Рассылка акций и новостей
    delivery_shares_news = models.BooleanField(verbose_name=_(u'Новости и Акции', ),
                                               default=True, )
    bad_email = models.BooleanField(verbose_name=_(u'Bad E-Mail', ),
                                    default=False, )
    error550 = models.BooleanField(verbose_name=_(u'Error 550', ),
                                   default=False, )
    error550_date = models.DateField(verbose_name=_(u'Error 550 Date', ),
                                     blank=True,
                                     null=True, )
    # Дата создания и дата обновления. Устанавливаются автоматически.
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name=_(u'Дата создания', ),
                                      blank=True,
                                      null=True, )
    updated_at = models.DateTimeField(auto_now=True, )

    def __str__(self):
        return '%d: %s' % (self.pk, self.email, )

    @property
    def domain(self, ):
        return self.email.split('@')[1]

    @property
    def content_type(self, ):
        return ContentType.objects.get_for_model(model=self, for_concrete_model=True, )

    class Meta:
        db_table = 'Delivery_SpamEmail'
        ordering = ['-created_at', ]
        verbose_name = u'Емэйл для спама'
        verbose_name_plural = u'Емэйлы для спама'


class SendEmailDelivery(models.Model, ):
    delivery = models.ForeignKey(to=Delivery,
                                 verbose_name=_(u'Указатель на рассылку', ),
                                 blank=False,
                                 null=False, )
    content_type = models.ForeignKey(ContentType,
                                     # related_name='email_instance',
                                     verbose_name=_(u'Указатель на E-Mail', ),
                                     blank=True,
                                     null=True, )
    object_id = models.PositiveIntegerField(db_index=True,
                                            blank=True,
                                            null=True, )
    email = GenericForeignKey('content_type', 'object_id', )

    #Дата создания и дата обновления. Устанавливаются автоматически.
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name=_(u'Дата создания', ),
                                      blank=True,
                                      null=True, )
    updated_at = models.DateTimeField(auto_now=True,
                                      verbose_name=_(u'Дата обновления', ),
                                      blank=True,
                                      null=True, )

    def __str__(self):
        return u'E-Mail: %s pk: %6d created_at: %s, updated_at: %s'\
               % (self.email.email, self.pk, self.created_at, self.updated_at, )

    class Meta:
        db_table = 'Delivery_SendEmailDelivery'
        ordering = ['-created_at', ]
        verbose_name = u'Рассылка отослана на (Email адрес)'
        verbose_name_plural = u'Рассылки отосланы на (Email адреса)'


class Message(models.Model):
    delivery = models.ForeignKey(to=Delivery,
                                 verbose_name=_(u'Указатель на рассылку', ),
                                 blank=False,
                                 null=False, )

    content_type = models.ForeignKey(ContentType,
                                     # related_name='email_instance',
                                     verbose_name=_(u'Указатель на E-Mail', ),
                                     blank=True,
                                     null=True, )
    object_id = models.PositiveIntegerField(db_index=True,
                                            blank=True,
                                            null=True, )
    email = GenericForeignKey('content_type', 'object_id', )

    direct_send = models.BooleanField(verbose_name=_(u'Шлем напрямую', ),
                                      blank=True,
                                      default=True, )
    direct_email = models.EmailField(verbose_name=_(u'E-Mail прямой отсылки', ),
                                     blank=True,
                                     null=True, )
    sender_account = models.ForeignKey(to=MailAccount,
                                       verbose_name=_(u'Account не прямой отсылки', ),
                                       blank=True,
                                       null=True, )

    subject = models.ForeignKey(to=Subject,
                                verbose_name=_(u'Указатель на subject', ),
                                blank=True,
                                null=True, )

    subject_str = models.CharField(max_length=256,
                                   verbose_name=_(u'Строка subject', ),
                                   blank=True,
                                   null=True, )



    #Дата создания и дата обновления. Устанавливаются автоматически.
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name=_(u'Дата создания', ),
                                      blank=True,
                                      null=True, )
    updated_at = models.DateTimeField(auto_now=True,
                                      verbose_name=_(u'Дата обновления', ),
                                      blank=True,
                                      null=True, )

    def __str__(self):
        return u'pk: %6d created_at: %s, updated_at: %s'\
               % (self.pk, self.created_at, self.updated_at, )

    class Meta:
        db_table = 'Delivery_Message'
        ordering = ['-created_at', ]
        verbose_name = u'Рассылка отослана на (Email адрес)'
        verbose_name_plural = u'Рассылки отосланы на (Email адреса)'


class MessageUrl(models.Model, ):
    delivery = models.ForeignKey(to=Delivery,
                                 verbose_name=_(u'Указатель на рассылку'),
                                 blank=False,
                                 null=False,)
    url = models.ForeignKey(to=Url,
                            verbose_name=_(u'Указатель на Url'),
                            blank=False,
                            null=False,)
    message = models.ForeignKey(to=Message,
                                verbose_name=_(u'Указатель на сообщение'),
                                blank=False,
                                null=False,)

    key = models.CharField(verbose_name=_(u'ID E-Mail адреса рассылки и Url', ),
                           max_length=64,
                           blank=False,
                           null=False,
                           default=hash_64, )

    content_type = models.ForeignKey(ContentType,
                                     # related_name='email_instance',
                                     verbose_name=_(u'Указатель на E-Mail', ),
                                     blank=True,
                                     null=True, )
    object_id = models.PositiveIntegerField(db_index=True,
                                            blank=True,
                                            null=True, )
    email = GenericForeignKey('content_type', 'object_id', )

    ready_url_str = models.CharField(verbose_name=_(u'Строка A tag', ),
                                     max_length=256,
                                     blank=False,
                                     null=False, )

    #Дата создания и дата обновления. Устанавливаются автоматически.
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name=_(u'Дата создания', ),
                                      blank=True,
                                      null=True, )
    updated_at = models.DateTimeField(auto_now=True,
                                      verbose_name=_(u'Дата обновления', ),
                                      blank=True,
                                      null=True, )

    def save(self, *args, **kwargs):

        if not self.key or len(self.key) < 64:
            while True:
                self.key = key(size=64, )
                try:
                    MessageUrl.objects.get(key=self.key, )
                except MessageUrl.DoesNotExist:
                    break
                except IntegrityError:
                    print('IntegrityError Key: %s' % self.key, )
                except Exception as e:
                    print('Exception type: %s, message: %s' % (type(e, ), e, ), )

        if not self.ready_url_str and self.url.type == 1:
            self.ready_url_str = render_to_string(
                template_name='render_url_string.jinja2',
                context={
                    'href': 'http://keksik.com.ua/delivery/redirect/',
                    'key': self.key,
                    'title': self.url.title,
                    'anchor': self.url.anchor,
                }, )

        elif not self.ready_url_str and self.url.type == 2:
            self.ready_url_str = render_to_string(
                template_name='render_unsub_url_string.jinja2',
                context={
                    'href': 'http://keksik.com.ua/delivery/redirect/',
                    'key': self.key,
                }, )

        elif not self.ready_url_str and self.url.type == 3:
            self.ready_url_str = render_to_string(
                template_name='render_open_img_string.jinja2',
                context={
                    'key': self.key,
                }, )

        super(MessageUrl, self).save(*args, **kwargs)

    def __str__(self):
        return u'pk: %0.6d --> [%s]' % (self.pk, self.email.email, )

    class Meta:
        db_table = 'Delivery_MessageUrl'
        ordering = ['-created_at', ]
        verbose_name = _(u'Message Url', )
        verbose_name_plural = _(u'Messages Urls', )


class RawEmail(models.Model, ):
    account = models.ForeignKey(to=MailAccount,
                                verbose_name=_(u'MailBox', ),
                                blank=True,
                                null=True, )

    message_id_header = models.CharField(verbose_name=_('Message-Id header'),
                                         max_length=255,
                                         blank=True,
                                         null=True, )

    from_header = models.CharField(verbose_name=_('From header'),
                                   max_length=255,
                                   blank=True,
                                   null=True, )

    to_header = models.TextField(verbose_name=_(u'To header'),
                                 blank=True,
                                 null=True, )

    subject_header = models.TextField(verbose_name=_(u'Subject header'),
                                      blank=True,
                                      null=True, )

    raw_email = models.TextField(verbose_name=_(u'Raw Email'),
                                 blank=True,
                                 null=True, )

    # Дата создания и дата обновления. Устанавливаются автоматически.
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name=_(u'Дата создания', ),
                                      blank=True,
                                      null=True, )
    updated_at = models.DateTimeField(auto_now=True, )

    def __str__(self):
        return u'RawEmail: pk: %6d, Account: %s From: <%s>, To: <%s> | created_at: %s, updated_at: %s'\
               % (self.pk, self.account.email, self.from_header, self.to_header, self.created_at, self.updated_at, )

    class Meta:
        db_table = 'Delivery_RawEmail'
        ordering = ['-created_at', ]
        verbose_name = u'RawЕмэйл'
        verbose_name_plural = u'RawЕмэйлы'
