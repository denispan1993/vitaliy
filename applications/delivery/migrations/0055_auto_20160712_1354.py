# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0054_auto_20160712_1323'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mailserver',
            old_name='is_active',
            new_name='use_smtp',
        ),
        migrations.AlterField(
            model_name='mailserver',
            name='server_smtp',
            field=models.CharField(max_length=128, null=True, verbose_name='SMTP Server', blank=True),
        ),
        migrations.AlterField(
            model_name='mailserver',
            name='use_ssl_smtp',
            field=models.BooleanField(default=False, verbose_name='SMTP Use SSL'),
        ),
        migrations.AlterField(
            model_name='mailserver',
            name='use_tls_smtp',
            field=models.BooleanField(default=True, verbose_name='SMTP Use TLS'),
        ),
    ]
