# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
import django.utils.datetime_safe


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0022_auto_20170424_2137'),
    ]

    operations = [
        migrations.AddField(
            model_name='producttocategory',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2017, 4, 24, 21, 39, 47, 503922), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='producttocategory',
            name='updated_at',
            field=models.DateTimeField(default=django.utils.datetime_safe.datetime.now, auto_now=True),
            preserve_default=False,
        ),
    ]
