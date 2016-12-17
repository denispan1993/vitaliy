# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sms_ussd', '0002_auto_20161217_1649'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sendsms',
            name='code',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='\u041a\u043e\u0434 \u043f\u0440\u043e\u0432\u0430\u0439\u0434\u0435\u0440\u0430', choices=[(39, b'\xd0\x9a\xd0\xb8\xd0\xb5\xd0\xb2\xd1\x81\xd1\x82\xd0\xb0\xd1\x80 (Golden Telecom)'), (50, b'Vodafone'), (63, b'Life:)'), (66, b'Vodafone'), (67, b'\xd0\x9a\xd0\xb8\xd0\xb5\xd0\xb2\xd1\x81\xd1\x82\xd0\xb0\xd1\x80'), (68, b'\xd0\x9a\xd0\xb8\xd0\xb5\xd0\xb2\xd1\x81\xd1\x82\xd0\xb0\xd1\x80 (Beeline)'), (91, b'Utel'), (92, b'PEOPLEnet'), (93, b'Life:)'), (94, b'\xd0\x98\xd0\xbd\xd1\x82\xd0\xb5\xd1\x80\xd1\x82\xd0\xb5\xd0\xbb\xd0\xb5\xd0\xba\xd0\xbe\xd0\xbc'), (95, b'Vodafone'), (96, b'\xd0\x9a\xd0\xb8\xd0\xb5\xd0\xb2\xd1\x81\xd1\x82\xd0\xb0\xd1\x80'), (97, b'\xd0\x9a\xd0\xb8\xd0\xb5\xd0\xb2\xd1\x81\xd1\x82\xd0\xb0\xd1\x80'), (98, b'\xd0\x9a\xd0\xb8\xd0\xb5\xd0\xb2\xd1\x81\xd1\x82\xd0\xb0\xd1\x80'), (99, b'Vodafone')]),
        ),
        migrations.AlterField(
            model_name='sendsms',
            name='phone',
            field=models.PositiveIntegerField(max_length=7, null=True, verbose_name='\u0422\u0435\u043b\u0435\u0444\u043e\u043d', blank=True),
        ),
    ]
