# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sms_ussd', '0013_auto_20161228_1545'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sim',
            name='imsi',
            field=models.BigIntegerField(unique=True, verbose_name='IMSI'),
        ),
    ]
