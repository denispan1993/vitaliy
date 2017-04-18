# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0018_auto_20170322_1639'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='barcode',
            field=models.CharField(help_text='\u0428\u0442\u0440\u0438\u0445\u043a\u043e\u0434', max_length=36, null=True, verbose_name='1C \u0428\u0442\u0440\u0438\u0445\u043a\u043e\u0434', blank=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='id_1c',
            field=models.CharField(help_text='\u041a\u043e\u0434 1\u0421', max_length=36, null=True, verbose_name='1C \u0418\u0434', blank=True),
        ),
    ]
