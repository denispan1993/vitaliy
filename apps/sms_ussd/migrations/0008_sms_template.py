# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sms_ussd', '0007_auto_20161223_1343'),
    ]

    operations = [
        migrations.AddField(
            model_name='sms',
            name='template',
            field=models.ForeignKey(verbose_name='Template', blank=True, to='sms_ussd.Template', null=True),
        ),
    ]
