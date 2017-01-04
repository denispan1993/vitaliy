# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import compat.bigint_path.bigint


class Migration(migrations.Migration):

    dependencies = [
        ('sms_ussd', '0019_auto_20170101_2014'),
    ]

    operations = [
        migrations.AddField(
            model_name='sms',
            name='sim',
            field=compat.bigint_path.bigint.BigForeignKey(verbose_name='SIM', blank=True, to='sms_ussd.SIM', null=True),
        ),
        migrations.AddField(
            model_name='ussd',
            name='sim',
            field=compat.bigint_path.bigint.BigForeignKey(verbose_name='SIM', blank=True, to='sms_ussd.SIM', null=True),
        ),
    ]
