# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-02 11:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0038_auto_20170702_0011'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='google_date',
        ),
        migrations.RemoveField(
            model_name='product',
            name='yandex_date',
        ),
        migrations.AddField(
            model_name='product',
            name='check_index_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Дата и время последней проверки индексации страницы'),
        ),
    ]
