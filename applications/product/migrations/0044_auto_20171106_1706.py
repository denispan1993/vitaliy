# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-11-06 15:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0043_auto_20171105_1104'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='is_left_vertical_column',
        ),
        migrations.AddField(
            model_name='category',
            name='serial_number_left_vertical_column',
            field=models.PositiveSmallIntegerField(blank=True, help_text='Порядковый номер в левой вертикальной колонке.', null=True, verbose_name='Левая вертикальная колонка'),
        ),
    ]
