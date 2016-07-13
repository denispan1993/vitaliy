# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0053_auto_20160712_1308'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mailserver',
            options={'ordering': ['-created_at'], 'verbose_name': 'Mail Server', 'verbose_name_plural': 'Mail Servers'},
        ),
        migrations.AlterField(
            model_name='mailserver',
            name='port_imap',
            field=models.PositiveSmallIntegerField(default=993, null=True, verbose_name='IMAP Port', blank=True),
        ),
        migrations.AlterField(
            model_name='mailserver',
            name='port_pop3',
            field=models.PositiveSmallIntegerField(default=995, null=True, verbose_name='POP3 Port', blank=True),
        ),
        migrations.AlterField(
            model_name='mailserver',
            name='port_smtp',
            field=models.PositiveSmallIntegerField(default=465, null=True, verbose_name='SMTP Port', blank=True),
        ),
    ]
