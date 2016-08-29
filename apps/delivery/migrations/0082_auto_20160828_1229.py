# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0081_auto_20160828_0319'),
    ]

    operations = [
        migrations.AddField(
            model_name='proxyserver',
            name='http_pos',
            field=models.IntegerField(null=True, verbose_name='HTTP pos', blank=True),
        ),
        migrations.AddField(
            model_name='proxyserver',
            name='https_pos',
            field=models.IntegerField(null=True, verbose_name='HTTPS pos', blank=True),
        ),
        migrations.AddField(
            model_name='proxyserver',
            name='socks4_pos',
            field=models.IntegerField(null=True, verbose_name='SOCKS4 pos', blank=True),
        ),
        migrations.AddField(
            model_name='proxyserver',
            name='socks5_pos',
            field=models.IntegerField(null=True, verbose_name='SOCKS5 pos', blank=True),
        ),
    ]
