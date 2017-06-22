# -*- coding: utf-8 -*-
__author__ = 'AlexStarov'
from django.db import models

# Create your models here.

from django.utils.translation import ugettext_lazy as _
from userena.models import UserenaBaseProfile, UserenaLanguageBaseProfile


class UserProfileModel(UserenaLanguageBaseProfile):
    # Пользователь
    # from django.contrib.auth.models import User
    # from django.contrib.auth import get_user_model
    # Users = get_user_model()
    from proj.settings import AUTH_USER_MODEL
    user = models.OneToOneField(AUTH_USER_MODEL,
                                unique=True,
                                verbose_name=_(u'Пользователь'),
                                related_name='user',
                                blank=False,
                                null=False, )
    """
        E-Mail рассылки
    """
    # Рассылка новых продуктов
#    email_delivery_new_products = models.BooleanField(verbose_name=_(u'Новые продукты', ),
#                                                      default=True, )
    # Рассылка акций и новостей
#    email_delivery_shares_news = models.BooleanField(verbose_name=_(u'Новости и Акции', ),
#                                                     default=True, )
    # Дата создания и дата обновления. Устанавливаются автоматически.
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True, )

    def __str__(self):
        return u'Профайл: %s' % (self.user, )

    class Meta:
        db_table = u'UserProfileModel'
        ordering = [u'-created_at', ]
        verbose_name = u'Профайл'
        verbose_name_plural = u'Профайлы'

#User.profile = property(lambda u: Profile.objects.get_or_create(user=u)[0])


class Session_ID(models.Model):
    """
        HttpRequest.META
    """
    # from django.contrib.auth.models import User
    from proj.settings import AUTH_USER_MODEL
    user = models.ForeignKey(AUTH_USER_MODEL,
                             verbose_name=u'Пользователь',
                             related_name='user_session_id',
                             null=True,
                             blank=True, )
    # from django.contrib.sessions.models import Session
    # session = models.ForeignKey(to=Session,
    #                             verbose_name=u'Session Foreign_Key',
    #                             null=True,
    #                             blank=True, )
    sessionid = models.CharField(verbose_name=u'SessionID',
                                 unique=True,
                                 max_length=32,
                                 null=True,
                                 blank=True, )

    #Дата создания и дата обновления. Устанавливаются автоматически.
    from datetime import datetime
    created_at = models.DateTimeField(auto_now_add=True, blank=False, null=False, )  #  default=datetime.now(), )
    updated_at = models.DateTimeField(auto_now=True, blank=False, null=False, )  # default=datetime.now(), )

    def __str__(self):
        return u'Связка:%s, session:%s' % (self.user, self.sessionid, )

    class Meta:
        db_table = u'Session_ID'
        ordering = [u'-created_at']
        verbose_name = u'Session_ID'
        verbose_name_plural = u'Session_ID'


class HttpRequest_META(models.Model):
    """
        HttpRequest.META
    """
    # from django.contrib.auth.models import User
    # user = models.ForeignKey(User,
    #                          verbose_name=u'Пользователь',
    #                          null=True,
    #                          blank=True, )
    # from django.contrib.sessions.models import Session
    # session = models.ForeignKey(to=Session,
    #                             verbose_name=u'Session Foreign_Key',
    #                             null=True,
    #                             blank=True, )
    # sessionid = models.CharField(verbose_name=u'SessionID',
    #                              max_length=32,
    #                              null=True,
    #                              blank=True, )

    session = models.ForeignKey(to=Session_ID,
                                verbose_name=u'Ссылка на session запись.',
                                blank=False,
                                null=False, )
    # CONTENT_LENGTH – the length of the request body (as a string).
    content_length = models.CharField(verbose_name='CONTENT_LENGTH',
                                      max_length=16,
                                      null=True,
                                      blank=True, )
    # CONTENT_TYPE – the MIME type of the request body.
    content_type = models.CharField(verbose_name='CONTENT_TYPE',
                                    max_length=16,
                                    null=True,
                                    blank=True, )
    # HTTP_ACCEPT_ENCODING – Acceptable encodings for the response.
    http_accept_encoding = models.CharField(verbose_name='HTTP_ACCEPT_ENCODING',
                                            max_length=16,
                                            null=True,
                                            blank=True, )
    # HTTP_ACCEPT_LANGUAGE – Acceptable languages for the response.
    http_accept_language = models.CharField(verbose_name='HTTP_ACCEPT_LANGUAGE',
                                            max_length=16,
                                            null=True,
                                            blank=True, )
    # HTTP_HOST – The HTTP Host header sent by the client.
    http_host = models.CharField(verbose_name='HTTP_HOST',
                                 max_length=16,
                                 null=True,
                                 blank=True, )
    # HTTP_REFERER – The referring page, if any.
    http_referer = models.CharField(verbose_name='HTTP_REFERER',
                                    max_length=16,
                                    null=True,
                                    blank=True, )
    # HTTP_USER_AGENT – The client’s user-agent string.
    http_user_agent = models.CharField(verbose_name='HTTP_USER_AGENT',
                                       max_length=16,
                                       null=True,
                                       blank=True, )
    # QUERY_STRING – The query string, as a single (unparsed) string.
    query_string = models.CharField(verbose_name='QUERY_STRING',
                                    max_length=16,
                                    null=True,
                                    blank=True, )
    # REMOTE_ADDR – The IP address of the client.
    remote_addr = models.CharField(verbose_name='REMOTE_ADDR',
                                   max_length=16,
                                   null=True,
                                   blank=True, )
    # REMOTE_HOST – The hostname of the client.
    remote_host = models.CharField(verbose_name='REMOTE_HOST',
                                   max_length=16,
                                   null=True,
                                   blank=True, )
    # REMOTE_USER – The user authenticated by the Web server, if any.
    remote_user = models.CharField(verbose_name='REMOTE_USER',
                                   max_length=16,
                                   null=True,
                                   blank=True, )
    # REQUEST_METHOD – A string such as "GET" or "POST".
    request_method = models.CharField(verbose_name='REMOTE_METHOD',
                                      max_length=16,
                                      null=True,
                                      blank=True, )
    # SERVER_NAME – The hostname of the server.
    server_name = models.CharField(verbose_name='SERVER_NAME',
                                   max_length=16,
                                   null=True,
                                   blank=True, )
    # SERVER_PORT – The port of the server (as a string).
    server_port = models.CharField(verbose_name='SERVER_PORT',
                                   max_length=16,
                                   null=True,
                                   blank=True, )

    #Дата создания и дата обновления. Устанавливаются автоматически.
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True, )

    def __str__(self):
        return u'Информация о первом входе:%s, session:%s' % (self.user, self.sessionid, )

    class Meta:
        db_table = u'HttpRequest_META'
        ordering = [u'-created_at']
        verbose_name = u'HttpRequest_META'
        verbose_name_plural = u'HttpRequest_META'
