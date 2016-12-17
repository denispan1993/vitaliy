# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SendSMS',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sessionid', models.CharField(max_length=32, null=True, verbose_name='SessionID', blank=True)),
                ('task_id', models.CharField(max_length=255, null=True, verbose_name='task id', blank=True)),
                ('send', models.BooleanField(default=False, verbose_name='\u041e\u0442\u043f\u0440\u0430\u0432\u043b\u0435\u043d\u043e')),
                ('code', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='\u041a\u043e\u0434 \u043f\u0440\u043e\u0432\u0430\u0439\u0434\u0435\u0440\u0430', choices=[(39, b'\xd0\x9a\xd0\xb8\xd0\xb5\xd0\xb2\xd1\x81\xd1\x82\xd0\xb0\xd1\x80 (Golden Telecom)'), (50, b'Vodafone'), (63, b'Life:)'), (66, b'Vodafone'), (67, b'\xd0\x9a\xd0\xb8\xd0\xb5\xd0\xb2\xd1\x81\xd1\x82\xd0\xb0\xd1\x80'), (68, b'\xd0\x9a\xd0\xb8\xd0\xb5\xd0\xb2\xd1\x81\xd1\x82\xd0\xb0\xd1\x80 (Beeline)'), (91, b'Utel'), (92, b'PEOPLEnet'), (93, b'Life:)'), (94, b'\xd0\x98\xd0\xbd\xd1\x82\xd0\xb5\xd1\x80\xd1\x82\xd0\xb5\xd0\xbb\xd0\xb5\xd0\xba\xd0\xbe\xd0\xbc'), (95, b'Vodafone'), (96, b'\xd0\x9a\xd0\xb8\xd0\xb5\xd0\xb2\xd1\x81\xd1\x82\xd0\xb0\xd1\x80'), (97, b'\xd0\x9a\xd0\xb8\xd0\xb5\xd0\xb2\xd1\x81\xd1\x82\xd0\xb0\xd1\x80'), (98, b'\xd0\x9a\xd0\xb8\xd0\xb5\xd0\xb2\xd1\x81\xd1\x82\xd0\xb0\xd1\x80'), (99, b'Vodafone')])),
                ('phone', models.CharField(max_length=7, null=True, verbose_name='\u0422\u0435\u043b\u0435\u0444\u043e\u043d', blank=True)),
                ('message', models.TextField(null=True, verbose_name='\u0421\u043e\u043e\u0431\u0449\u0435\u043d\u0438\u0435', blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='\u0414\u0430\u0442\u0430 \u0441\u043e\u0437\u0434\u0430\u043d\u0438\u044f', null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='\u0414\u0430\u0442\u0430 \u043e\u0431\u043d\u043e\u0432\u043b\u0435\u043d\u0438\u044f', null=True)),
                ('user', models.ForeignKey(verbose_name='\u041f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044c', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ['-created_at'],
                'db_table': 'SMS_USSD_SendSMS',
                'verbose_name': 'SendSMS',
                'verbose_name_plural': 'SendSMS',
            },
        ),
    ]
