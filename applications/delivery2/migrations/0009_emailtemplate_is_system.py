# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-20 09:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery2', '0008_remove_emailtemplate_is_system'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailtemplate',
            name='is_system',
            field=models.BooleanField(default=False, verbose_name='Системный'),
        ),
    ]
