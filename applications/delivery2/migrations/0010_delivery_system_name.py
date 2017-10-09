# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-06 10:27
from __future__ import unicode_literals

import applications.delivery2.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery2', '0009_emailtemplate_is_system'),
    ]

    operations = [
        migrations.AddField(
            model_name='delivery',
            name='system_name',
            field=models.CharField(blank=True, default=applications.delivery2.models.datetime_in_iso_format, max_length=128, null=True, verbose_name='Имя системной рассылки'),
        ),
    ]