# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-08 13:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0040_producttocategory_is_main'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='location',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Не задано'), (1, 'Верх'), (2, 'Низ')], default=0, verbose_name='Положение'),
        ),
    ]