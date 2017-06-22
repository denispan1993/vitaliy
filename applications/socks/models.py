# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
import sockschain as socks

__author__ = 'AlexStarov'


class ProxyServer(models.Model, ):

    hosts = (
        (1, _(u'http://hideme.ru', ), ),
        (2, _(u'http://socks-proxy.net', ), ),
        (3, _(u'http://gatherproxy.com', ), ),
    )

    from_whence = models.PositiveSmallIntegerField(verbose_name=_(u'Откуда', ),
                                                   choices=hosts,
                                                   blank=False,
                                                   null=False,)

    host = models.CharField(verbose_name=_(u'Host', ),
                            max_length=15,
                            blank=False,
                            null=False,
                            default=_(u'000.000.000.000', ), )

    port = models.PositiveIntegerField(verbose_name=_(u'Port', ),
                                       blank=False,
                                       null=False,
                                       default=1080, )

    http = models.BooleanField(verbose_name=_(u'HTTP'),
                               default=False, )
    http_pos = models.IntegerField(verbose_name=_(u'HTTP pos'),
                                   blank=True,
                                   null=True, )
    https = models.BooleanField(verbose_name=_(u'HTTPS'),
                                default=False, )
    https_pos = models.IntegerField(verbose_name=_(u'HTTPS pos'),
                                    blank=True,
                                    null=True, )

    socks4 = models.BooleanField(verbose_name=_(u'SOCK4'),
                                 default=False, )
    socks4_pos = models.IntegerField(verbose_name=_(u'SOCKS4 pos'),
                                     blank=True,
                                     null=True, )

    socks4_success = models.IntegerField(
        verbose_name=_(u'SOCKS4 success'),
        blank=True,
        null=True, )

    socks5 = models.BooleanField(verbose_name=_(u'SOCK5'),
                                default=False, )
    socks5_pos = models.IntegerField(verbose_name=_(u'SOCKS5 pos'),
                                     blank=True,
                                     null=True, )

    socks5_success = models.IntegerField(
        verbose_name=_(u'SOCKS5 success'),
        blank=True,
        null=True, )

    failed = models.IntegerField(
        verbose_name=_(u'failed'),
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

    def dec_pos(self, proxy_type=socks.PROXY_TYPE_HTTP, int_dec=1):

        if proxy_type == socks.PROXY_TYPE_HTTP:
            print('proxy_type == socks.PROXY_TYPE_HTTP')
            try:
                self.http_pos -= int_dec
            except TypeError:
                self.http_pos = -int_dec
        elif proxy_type == socks.PROXY_TYPE_HTTPS:
            print('proxy_type == socks.PROXY_TYPE_HTTPS')
            try:
                self.https_pos -= int_dec
            except TypeError:
                self.https_pos = -int_dec
        elif proxy_type == socks.PROXY_TYPE_SOCKS4:
            try:
                self.socks4_pos -= int_dec
            except TypeError:
                self.socks4_pos = -int_dec
            print('proxy_type == socks.PROXY_TYPE_SOCKS4: ', 'self.socks4_pos: ', self.socks4_pos)
        elif proxy_type == socks.PROXY_TYPE_SOCKS5:
            try:
                self.socks5_pos -= int_dec
            except TypeError:
                self.socks5_pos = -int_dec
            print('proxy_type == socks.PROXY_TYPE_SOCKS5: ', 'self.socks5_pos: ', self.socks5_pos)
        self.save()

    def inc_pos(self, proxy_type=socks.PROXY_TYPE_HTTP, int_inc=1, ):

        if proxy_type == socks.PROXY_TYPE_HTTP:
            print('proxy_type == socks.PROXY_TYPE_HTTP')
            try:
                self.http_pos += int_inc
            except TypeError:
                self.http_pos = int_inc
        elif proxy_type == socks.PROXY_TYPE_HTTPS:
            print('proxy_type == socks.PROXY_TYPE_HTTPS')
            try:
                self.https_pos += int_inc
            except TypeError:
                self.https_pos = int_inc
        elif proxy_type == socks.PROXY_TYPE_SOCKS4:
            try:
                self.socks4_pos += int_inc
            except TypeError:
                self.socks4_pos = int_inc
            print('proxy_type == socks.PROXY_TYPE_SOCKS4: ', 'self.socks4_pos: ', self.socks4_pos)
        elif proxy_type == socks.PROXY_TYPE_SOCKS5:
            try:
                self.socks5_pos += int_inc
            except TypeError:
                self.socks5_pos = int_inc
            print('proxy_type == socks.PROXY_TYPE_SOCKS5: ', 'self.socks5_pos: ', self.socks5_pos)
        self.save()

    def __str__(self):
        return u'№ %6d --> [%s:%s] http: %s | https: %s | socks4: %s | socks5: %s'\
               % (self.pk, self.host, self.port, self.http, self.https, self.socks4, self.socks5, )

    class Meta:
        db_table = 'Delivery_ProxyServer'
        ordering = ['-created_at', ]
        verbose_name = _(u'ProxyServer', )
        verbose_name_plural = _(u'ProxyServers', )
