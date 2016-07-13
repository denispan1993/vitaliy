# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('captcha', '0003_auto_20160507_2145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='captcha_key',
            name='next_use',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
