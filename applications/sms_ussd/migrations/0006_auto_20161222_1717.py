# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sms_ussd', '0005_auto_20161221_1719'),
    ]

    operations = [
        migrations.AddField(
            model_name='sms',
            name='from_phone_char',
            field=models.CharField(max_length=16, null=True, verbose_name='\u041d\u043e\u043c\u0435\u0440 \u0442\u0435\u043b\u0435\u0444\u043e\u043d\u0430 (\u041e\u0442\u043a\u0443\u0434\u0430)', blank=True),
        ),
        migrations.AddField(
            model_name='sms',
            name='to_phone_char',
            field=models.CharField(max_length=16, null=True, verbose_name='\u041d\u043e\u043c\u0435\u0440 \u0442\u0435\u043b\u0435\u0444\u043e\u043d\u0430 (\u041a\u0443\u0434\u0430)', blank=True),
        ),
    ]
