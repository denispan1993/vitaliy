# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sms_ussd', '0006_auto_20161222_1717'),
    ]

    operations = [
        migrations.AddField(
            model_name='sms',
            name='direction',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='\u041d\u0430\u043f\u0440\u0430\u0432\u043b\u0435\u043d\u0438\u0435', choices=[(1, b'Incoming'), (2, b'Outgoing')]),
        ),
        migrations.AddField(
            model_name='sms',
            name='send_at',
            field=models.DateTimeField(null=True, verbose_name='\u0414\u0430\u0442\u0430 \u0438 \u0432\u0440\u0435\u043c\u044f \u043e\u0442\u043f\u0440\u0430\u0432\u043a\u0438 SMS', blank=True),
        ),
    ]
