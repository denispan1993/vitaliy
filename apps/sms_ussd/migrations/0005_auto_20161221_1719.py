# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('sms_ussd', '0004_auto_20161219_1719'),
    ]

    operations = [
        migrations.CreateModel(
            name='Template',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(null=True, default=datetime.datetime.now, max_length=64, blank=True, unique=True, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
                ('is_system', models.BooleanField(default=False, verbose_name='\u0421\u0438\u0441\u0442\u0435\u043c\u043d\u044b\u0439')),
                ('template', models.TextField(null=True, verbose_name='\u0428\u0430\u0431\u043b\u043e\u043d', blank=True)),
                ('chance', models.DecimalField(default=1, verbose_name='\u0412\u0435\u0440\u043e\u044f\u0442\u043d\u043e\u0441\u0442\u044c', max_digits=4, decimal_places=2)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='\u0414\u0430\u0442\u0430 \u0441\u043e\u0437\u0434\u0430\u043d\u0438\u044f', null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='\u0414\u0430\u0442\u0430 \u043e\u0431\u043d\u043e\u0432\u043b\u0435\u043d\u0438\u044f', null=True)),
            ],
            options={
                'ordering': ['-created_at'],
                'db_table': 'SMS_USSD__Template',
                'verbose_name': 'Template',
                'verbose_name_plural': 'Template',
            },
        ),
        migrations.AlterModelOptions(
            name='sms',
            options={'ordering': ['-created_at'], 'verbose_name': 'SMS', 'verbose_name_plural': 'SMS'},
        ),
        migrations.RenameField(
            model_name='sms',
            old_name='code',
            new_name='from_code',
        ),
        migrations.RenameField(
            model_name='sms',
            old_name='phone',
            new_name='from_phone',
        ),
        migrations.AddField(
            model_name='sms',
            name='received_at',
            field=models.DateTimeField(null=True, verbose_name='\u0414\u0430\u0442\u0430 \u0438 \u0432\u0440\u0435\u043c\u044f \u043f\u043e\u043b\u0443\u0447\u0435\u043d\u0438\u044f SMS', blank=True),
        ),
        migrations.AddField(
            model_name='sms',
            name='to_code',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='\u041a\u043e\u0434 \u043f\u0440\u043e\u0432\u0430\u0439\u0434\u0435\u0440\u0430', choices=[(39, b'039 ==> \xd0\x9a\xd0\xb8\xd0\xb5\xd0\xb2\xd1\x81\xd1\x82\xd0\xb0\xd1\x80 (Golden Telecom)'), (50, b'050 ==> Vodafone'), (63, b'063 ==> Life:)'), (66, b'066 ==> Vodafone'), (67, b'067 ==> \xd0\x9a\xd0\xb8\xd0\xb5\xd0\xb2\xd1\x81\xd1\x82\xd0\xb0\xd1\x80'), (68, b'068 ==> \xd0\x9a\xd0\xb8\xd0\xb5\xd0\xb2\xd1\x81\xd1\x82\xd0\xb0\xd1\x80 (Beeline)'), (91, b'091 ==> Utel'), (92, b'092 ==> PEOPLEnet'), (93, b'093 ==> Life:)'), (94, b'094 ==> \xd0\x98\xd0\xbd\xd1\x82\xd0\xb5\xd1\x80\xd1\x82\xd0\xb5\xd0\xbb\xd0\xb5\xd0\xba\xd0\xbe\xd0\xbc'), (95, b'095 ==> Vodafone'), (96, b'096 ==> \xd0\x9a\xd0\xb8\xd0\xb5\xd0\xb2\xd1\x81\xd1\x82\xd0\xb0\xd1\x80'), (97, b'097 ==> \xd0\x9a\xd0\xb8\xd0\xb5\xd0\xb2\xd1\x81\xd1\x82\xd0\xb0\xd1\x80'), (98, b'098 ==> \xd0\x9a\xd0\xb8\xd0\xb5\xd0\xb2\xd1\x81\xd1\x82\xd0\xb0\xd1\x80'), (99, b'099 ==> Vodafone')]),
        ),
        migrations.AddField(
            model_name='sms',
            name='to_phone',
            field=models.PositiveIntegerField(null=True, verbose_name='\u0422\u0435\u043b\u0435\u0444\u043e\u043d', blank=True),
        ),
    ]
