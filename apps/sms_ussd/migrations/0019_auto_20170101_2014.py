# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import compat.bigint_path.bigint


class Migration(migrations.Migration):

    dependencies = [
        ('sms_ussd', '0018_auto_20170101_2001'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sms',
            name='sim',
        ),
        migrations.RemoveField(
            model_name='ussd',
            name='sim',
        ),
        migrations.RemoveField(
            model_name='sim',
            name='id',
        ),
        migrations.AlterField(
            model_name='sim',
            name='imsi',
            field=compat.bigint_path.bigint.BigIntegerField(unique=True, serialize=False, verbose_name='IMSI', primary_key=True),
        ),
    ]
