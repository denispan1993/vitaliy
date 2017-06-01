# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sms_ussd', '0014_auto_20161228_1558'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sms',
            name='sim',
        ),
        migrations.RemoveField(
            model_name='sms',
            name='template',
        ),
        migrations.RemoveField(
            model_name='sms',
            name='user',
        ),
        migrations.RemoveField(
            model_name='ussd',
            name='sim',
        ),
        migrations.RemoveField(
            model_name='ussd',
            name='user',
        ),
        migrations.DeleteModel(
            name='SIM',
        ),
        migrations.DeleteModel(
            name='SMS',
        ),
        migrations.DeleteModel(
            name='USSD',
        ),
    ]
