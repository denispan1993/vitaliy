# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-07 18:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('callback', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='callback',
            name='phone',
            field=models.CharField(default='phone number', max_length=32, verbose_name='Номер телефона'),
        ),
    ]