# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-05 18:03
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0010_auto_20170625_2331'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_order', related_query_name='order_user', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
    ]
