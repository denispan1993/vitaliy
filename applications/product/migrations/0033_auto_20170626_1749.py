# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-26 14:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0032_auto_20170626_1749'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, db_index=True),
        ),
    ]
