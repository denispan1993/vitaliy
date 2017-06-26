# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-26 14:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0033_auto_20170626_1749'),
    ]

    operations = [
        migrations.AlterField(
            model_name='currency',
            name='currency_code_ISO_char',
            field=models.CharField(default='UAH', max_length=3, verbose_name='Код валюты буквенный'),
        ),
        migrations.AlterField(
            model_name='currency',
            name='currency_code_ISO_number',
            field=models.PositiveSmallIntegerField(db_index=True, default=0, verbose_name='Код валюты числовой'),
        ),
    ]
