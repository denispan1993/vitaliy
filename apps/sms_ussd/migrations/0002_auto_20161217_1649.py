# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sms_ussd', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sendsms',
            name='code',
            field=models.CharField(blank=True, max_length=4, null=True, verbose_name='\u041a\u043e\u0434 \u043f\u0440\u043e\u0432\u0430\u0439\u0434\u0435\u0440\u0430', choices=[(39, b'\xd0\x9a\xd0\xb8\xd0\xb5\xd0\xb2\xd1\x81\xd1\x82\xd0\xb0\xd1\x80 (Golden Telecom)'), (50, b'Vodafone'), (63, b'Life:)'), (66, b'Vodafone'), (67, b'\xd0\x9a\xd0\xb8\xd0\xb5\xd0\xb2\xd1\x81\xd1\x82\xd0\xb0\xd1\x80'), (68, b'\xd0\x9a\xd0\xb8\xd0\xb5\xd0\xb2\xd1\x81\xd1\x82\xd0\xb0\xd1\x80 (Beeline)'), (91, b'Utel'), (92, b'PEOPLEnet'), (93, b'Life:)'), (94, b'\xd0\x98\xd0\xbd\xd1\x82\xd0\xb5\xd1\x80\xd1\x82\xd0\xb5\xd0\xbb\xd0\xb5\xd0\xba\xd0\xbe\xd0\xbc'), (95, b'Vodafone'), (96, b'\xd0\x9a\xd0\xb8\xd0\xb5\xd0\xb2\xd1\x81\xd1\x82\xd0\xb0\xd1\x80'), (97, b'\xd0\x9a\xd0\xb8\xd0\xb5\xd0\xb2\xd1\x81\xd1\x82\xd0\xb0\xd1\x80'), (98, b'\xd0\x9a\xd0\xb8\xd0\xb5\xd0\xb2\xd1\x81\xd1\x82\xd0\xb0\xd1\x80'), (99, b'Vodafone')]),
        ),
    ]
