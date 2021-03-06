# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-26 14:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0034_auto_20170626_1750'),
    ]

    operations = [
        migrations.AlterField(
            model_name='manufacturer',
            name='name',
            field=models.CharField(blank=True, default='', max_length=128, null=True, verbose_name='Наименование производителя'),
        ),
        migrations.AlterField(
            model_name='photo',
            name='serial_number',
            field=models.PositiveIntegerField(db_index=True, default=1, verbose_name='Порядковы номер фотографии'),
        ),
    ]
