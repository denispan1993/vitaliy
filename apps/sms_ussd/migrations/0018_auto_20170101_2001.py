# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sms_ussd', '0017_sms_message_pdu'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sim',
            name='imsi',
            field=models.BigIntegerField(verbose_name='IMSI'),
        ),
        migrations.AlterField(
            model_name='sim',
            name='name',
            field=models.CharField(max_length=16, unique=True, null=True, verbose_name='\u0418\u043c\u044f \u0443\u0441\u0442\u0440\u043e\u0439\u0441\u0442\u0432\u0430', blank=True),
        ),
    ]
