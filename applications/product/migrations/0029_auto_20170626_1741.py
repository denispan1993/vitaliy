# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-26 14:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0028_auto_20170530_1508'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Unit_of_Measurement',
            new_name='UnitofMeasurement',
        ),
    ]
