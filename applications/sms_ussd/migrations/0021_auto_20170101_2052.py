# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sms_ussd', '0020_auto_20170101_2029'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ussd',
            name='phone',
        ),
        migrations.RemoveField(
            model_name='ussd',
            name='phone_char',
        ),
        migrations.RemoveField(
            model_name='ussd',
            name='phone_code',
        ),
    ]
