# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-06 10:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery2', '0010_delivery_system_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='delivery',
            name='is_system',
            field=models.BooleanField(default=False, verbose_name='Рассылка системная'),
        ),
    ]
