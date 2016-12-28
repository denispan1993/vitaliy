# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sms_ussd', '0011_auto_20161228_1539'),
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
        migrations.DeleteModel(
            name='SIM',
        ),
    ]
