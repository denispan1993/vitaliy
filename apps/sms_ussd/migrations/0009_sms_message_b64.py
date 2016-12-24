# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sms_ussd', '0008_sms_template'),
    ]

    operations = [
        migrations.AddField(
            model_name='sms',
            name='message_b64',
            field=models.TextField(null=True, verbose_name='\u0421\u043e\u043e\u0431\u0449\u0435\u043d\u0438\u0435 base64', blank=True),
        ),
    ]
