# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sms_ussd', '0010_auto_20161227_2305'),
    ]

    operations = [
        migrations.CreateModel(
            name='SIM',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=16, null=True, verbose_name='\u0418\u043c\u044f \u0443\u0441\u0442\u0440\u043e\u0439\u0441\u0442\u0432\u0430', blank=True)),
                ('phone', models.CharField(max_length=14, null=True, verbose_name='\u041d\u043e\u043c\u0435\u0440 \u0442\u0435\u043b\u0435\u0444\u043e\u043d\u0430', blank=True)),
                ('provider', models.CharField(max_length=14, null=True, verbose_name='\u041f\u0440\u043e\u0432\u0430\u0439\u0434\u0435\u0440', blank=True)),
                ('imsi', models.CharField(max_length=15, null=True, verbose_name='IMSI', blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='\u0414\u0430\u0442\u0430 \u0441\u043e\u0437\u0434\u0430\u043d\u0438\u044f', null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='\u0414\u0430\u0442\u0430 \u043e\u0431\u043d\u043e\u0432\u043b\u0435\u043d\u0438\u044f', null=True)),
            ],
            options={
                'ordering': ['-created_at'],
                'db_table': 'SMS_USSD__SIM',
                'verbose_name': 'SIM',
                'verbose_name_plural': 'SIM',
            },
        ),
        migrations.RemoveField(
            model_name='ussd',
            name='from_device',
        ),
        migrations.AddField(
            model_name='ussd',
            name='phone',
            field=models.PositiveIntegerField(null=True, verbose_name='\u0422\u0435\u043b\u0435\u0444\u043e\u043d', blank=True),
        ),
        migrations.AddField(
            model_name='ussd',
            name='phone_char',
            field=models.CharField(max_length=64, null=True, verbose_name='\u041d\u043e\u043c\u0435\u0440 \u0442\u0435\u043b\u0435\u0444\u043e\u043d\u0430 (\u041a\u0443\u0434\u0430)', blank=True),
        ),
        migrations.AddField(
            model_name='ussd',
            name='phone_code',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='\u041a\u043e\u0434 \u043f\u0440\u043e\u0432\u0430\u0439\u0434\u0435\u0440\u0430', choices=[(39, b'039 ==> \xd0\x9a\xd0\xb8\xd0\xb5\xd0\xb2\xd1\x81\xd1\x82\xd0\xb0\xd1\x80 (Golden Telecom)'), (50, b'050 ==> Vodafone'), (63, b'063 ==> Life:)'), (66, b'066 ==> Vodafone'), (67, b'067 ==> \xd0\x9a\xd0\xb8\xd0\xb5\xd0\xb2\xd1\x81\xd1\x82\xd0\xb0\xd1\x80'), (68, b'068 ==> \xd0\x9a\xd0\xb8\xd0\xb5\xd0\xb2\xd1\x81\xd1\x82\xd0\xb0\xd1\x80 (Beeline)'), (91, b'091 ==> Utel'), (92, b'092 ==> PEOPLEnet'), (93, b'093 ==> Life:)'), (94, b'094 ==> \xd0\x98\xd0\xbd\xd1\x82\xd0\xb5\xd1\x80\xd1\x82\xd0\xb5\xd0\xbb\xd0\xb5\xd0\xba\xd0\xbe\xd0\xbc'), (95, b'095 ==> Vodafone'), (96, b'096 ==> \xd0\x9a\xd0\xb8\xd0\xb5\xd0\xb2\xd1\x81\xd1\x82\xd0\xb0\xd1\x80'), (97, b'097 ==> \xd0\x9a\xd0\xb8\xd0\xb5\xd0\xb2\xd1\x81\xd1\x82\xd0\xb0\xd1\x80'), (98, b'098 ==> \xd0\x9a\xd0\xb8\xd0\xb5\xd0\xb2\xd1\x81\xd1\x82\xd0\xb0\xd1\x80'), (99, b'099 ==> Vodafone')]),
        ),
        migrations.AddField(
            model_name='sms',
            name='sim',
            field=models.ForeignKey(verbose_name='SIM', blank=True, to='sms_ussd.SIM', null=True),
        ),
        migrations.AddField(
            model_name='ussd',
            name='sim',
            field=models.ForeignKey(verbose_name='SIM', blank=True, to='sms_ussd.SIM', null=True),
        ),
    ]
