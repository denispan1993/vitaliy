# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-07 18:51
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import re


class Migration(migrations.Migration):

    dependencies = [
        ('authModel', '0009_auto_20161224_1946'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(help_text='Required. 32 characters or fewer. Letters, numbers and @/./+/-/_ characters', max_length=32, unique=True, validators=[django.core.validators.RegexValidator(re.compile('^[\\w.@+-]+$', 32), 'Enter a valid username.', 'invalid')], verbose_name='username'),
        ),
    ]