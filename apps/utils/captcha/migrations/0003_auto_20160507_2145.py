# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('captcha', '0002_auto_20160505_2146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='captcha_key',
            name='next_use',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 7, 21, 45, 36, 415470)),
        ),
    ]
