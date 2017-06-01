# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sms_ussd', '0015_auto_20161230_1923'),
    ]

    operations = [
        migrations.CreateModel(
            name='SIM',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=16, null=True, verbose_name='\u0418\u043c\u044f \u0443\u0441\u0442\u0440\u043e\u0439\u0441\u0442\u0432\u0430', blank=True)),
                ('phone', models.CharField(max_length=14, null=True, verbose_name='\u041d\u043e\u043c\u0435\u0440 \u0442\u0435\u043b\u0435\u0444\u043e\u043d\u0430', blank=True)),
                ('provider', models.CharField(max_length=14, null=True, verbose_name='\u041f\u0440\u043e\u0432\u0430\u0439\u0434\u0435\u0440', blank=True)),
                ('imsi', models.IntegerField(unique=True, verbose_name='IMSI')),
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
        migrations.CreateModel(
            name='SMS',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('direction', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='\u041d\u0430\u043f\u0440\u0430\u0432\u043b\u0435\u043d\u0438\u0435', choices=[(1, b'Incoming'), (2, b'Outgoing')])),
                ('sessionid', models.CharField(max_length=32, null=True, verbose_name='SessionID', blank=True)),
                ('task_id', models.CharField(max_length=255, null=True, verbose_name='task id', blank=True)),
                ('is_send', models.BooleanField(default=False, verbose_name='\u041e\u0442\u043f\u0440\u0430\u0432\u043b\u0435\u043d\u043e')),
                ('from_phone_char', models.CharField(max_length=64, null=True, verbose_name='\u041d\u043e\u043c\u0435\u0440 \u0442\u0435\u043b\u0435\u0444\u043e\u043d\u0430 (\u041e\u0442\u043a\u0443\u0434\u0430)', blank=True)),
                ('from_code', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='\u041a\u043e\u0434 \u043f\u0440\u043e\u0432\u0430\u0439\u0434\u0435\u0440\u0430', choices=[(39, b'039 ==> \xd0\x9a\xd0\xb8\xd0\xb5\xd0\xb2\xd1\x81\xd1\x82\xd0\xb0\xd1\x80 (Golden Telecom)'), (50, b'050 ==> Vodafone'), (63, b'063 ==> Life:)'), (66, b'066 ==> Vodafone'), (67, b'067 ==> \xd0\x9a\xd0\xb8\xd0\xb5\xd0\xb2\xd1\x81\xd1\x82\xd0\xb0\xd1\x80'), (68, b'068 ==> \xd0\x9a\xd0\xb8\xd0\xb5\xd0\xb2\xd1\x81\xd1\x82\xd0\xb0\xd1\x80 (Beeline)'), (91, b'091 ==> Utel'), (92, b'092 ==> PEOPLEnet'), (93, b'093 ==> Life:)'), (94, b'094 ==> \xd0\x98\xd0\xbd\xd1\x82\xd0\xb5\xd1\x80\xd1\x82\xd0\xb5\xd0\xbb\xd0\xb5\xd0\xba\xd0\xbe\xd0\xbc'), (95, b'095 ==> Vodafone'), (96, b'096 ==> \xd0\x9a\xd0\xb8\xd0\xb5\xd0\xb2\xd1\x81\xd1\x82\xd0\xb0\xd1\x80'), (97, b'097 ==> \xd0\x9a\xd0\xb8\xd0\xb5\xd0\xb2\xd1\x81\xd1\x82\xd0\xb0\xd1\x80'), (98, b'098 ==> \xd0\x9a\xd0\xb8\xd0\xb5\xd0\xb2\xd1\x81\xd1\x82\xd0\xb0\xd1\x80'), (99, b'099 ==> Vodafone')])),
                ('from_phone', models.PositiveIntegerField(null=True, verbose_name='\u0422\u0435\u043b\u0435\u0444\u043e\u043d', blank=True)),
                ('to_phone_char', models.CharField(max_length=64, null=True, verbose_name='\u041d\u043e\u043c\u0435\u0440 \u0442\u0435\u043b\u0435\u0444\u043e\u043d\u0430 (\u041a\u0443\u0434\u0430)', blank=True)),
                ('to_code', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='\u041a\u043e\u0434 \u043f\u0440\u043e\u0432\u0430\u0439\u0434\u0435\u0440\u0430', choices=[(39, b'039 ==> \xd0\x9a\xd0\xb8\xd0\xb5\xd0\xb2\xd1\x81\xd1\x82\xd0\xb0\xd1\x80 (Golden Telecom)'), (50, b'050 ==> Vodafone'), (63, b'063 ==> Life:)'), (66, b'066 ==> Vodafone'), (67, b'067 ==> \xd0\x9a\xd0\xb8\xd0\xb5\xd0\xb2\xd1\x81\xd1\x82\xd0\xb0\xd1\x80'), (68, b'068 ==> \xd0\x9a\xd0\xb8\xd0\xb5\xd0\xb2\xd1\x81\xd1\x82\xd0\xb0\xd1\x80 (Beeline)'), (91, b'091 ==> Utel'), (92, b'092 ==> PEOPLEnet'), (93, b'093 ==> Life:)'), (94, b'094 ==> \xd0\x98\xd0\xbd\xd1\x82\xd0\xb5\xd1\x80\xd1\x82\xd0\xb5\xd0\xbb\xd0\xb5\xd0\xba\xd0\xbe\xd0\xbc'), (95, b'095 ==> Vodafone'), (96, b'096 ==> \xd0\x9a\xd0\xb8\xd0\xb5\xd0\xb2\xd1\x81\xd1\x82\xd0\xb0\xd1\x80'), (97, b'097 ==> \xd0\x9a\xd0\xb8\xd0\xb5\xd0\xb2\xd1\x81\xd1\x82\xd0\xb0\xd1\x80'), (98, b'098 ==> \xd0\x9a\xd0\xb8\xd0\xb5\xd0\xb2\xd1\x81\xd1\x82\xd0\xb0\xd1\x80'), (99, b'099 ==> Vodafone')])),
                ('to_phone', models.PositiveIntegerField(null=True, verbose_name='\u0422\u0435\u043b\u0435\u0444\u043e\u043d', blank=True)),
                ('message', models.TextField(null=True, verbose_name='\u0421\u043e\u043e\u0431\u0449\u0435\u043d\u0438\u0435', blank=True)),
                ('message_b64', models.TextField(null=True, verbose_name='\u0421\u043e\u043e\u0431\u0449\u0435\u043d\u0438\u0435 base64', blank=True)),
                ('send_at', models.DateTimeField(null=True, verbose_name='\u0414\u0430\u0442\u0430 \u0438 \u0432\u0440\u0435\u043c\u044f \u043e\u0442\u043f\u0440\u0430\u0432\u043a\u0438 SMS', blank=True)),
                ('received_at', models.DateTimeField(null=True, verbose_name='\u0414\u0430\u0442\u0430 \u0438 \u0432\u0440\u0435\u043c\u044f \u043f\u043e\u043b\u0443\u0447\u0435\u043d\u0438\u044f SMS', blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='\u0414\u0430\u0442\u0430 \u0441\u043e\u0437\u0434\u0430\u043d\u0438\u044f', null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='\u0414\u0430\u0442\u0430 \u043e\u0431\u043d\u043e\u0432\u043b\u0435\u043d\u0438\u044f', null=True)),
                ('sim', models.ForeignKey(verbose_name='SIM', blank=True, to='sms_ussd.SIM', null=True)),
                ('template', models.ForeignKey(verbose_name='Template', blank=True, to='sms_ussd.Template', null=True)),
                ('user', models.ForeignKey(verbose_name='\u041f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044c', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ['-created_at'],
                'db_table': 'SMS_USSD__SMS',
                'verbose_name': 'SMS',
                'verbose_name_plural': 'SMS',
            },
        ),
        migrations.CreateModel(
            name='USSD',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('direction', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='\u041d\u0430\u043f\u0440\u0430\u0432\u043b\u0435\u043d\u0438\u0435', choices=[(1, b'Receive'), (2, b'Send')])),
                ('sessionid', models.CharField(max_length=32, null=True, verbose_name='SessionID', blank=True)),
                ('task_id', models.CharField(max_length=255, null=True, verbose_name='task.id', blank=True)),
                ('phone_char', models.CharField(max_length=64, null=True, verbose_name='\u041d\u043e\u043c\u0435\u0440 \u0442\u0435\u043b\u0435\u0444\u043e\u043d\u0430 (\u041a\u0443\u0434\u0430)', blank=True)),
                ('phone_code', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='\u041a\u043e\u0434 \u043f\u0440\u043e\u0432\u0430\u0439\u0434\u0435\u0440\u0430', choices=[(39, b'039 ==> \xd0\x9a\xd0\xb8\xd0\xb5\xd0\xb2\xd1\x81\xd1\x82\xd0\xb0\xd1\x80 (Golden Telecom)'), (50, b'050 ==> Vodafone'), (63, b'063 ==> Life:)'), (66, b'066 ==> Vodafone'), (67, b'067 ==> \xd0\x9a\xd0\xb8\xd0\xb5\xd0\xb2\xd1\x81\xd1\x82\xd0\xb0\xd1\x80'), (68, b'068 ==> \xd0\x9a\xd0\xb8\xd0\xb5\xd0\xb2\xd1\x81\xd1\x82\xd0\xb0\xd1\x80 (Beeline)'), (91, b'091 ==> Utel'), (92, b'092 ==> PEOPLEnet'), (93, b'093 ==> Life:)'), (94, b'094 ==> \xd0\x98\xd0\xbd\xd1\x82\xd0\xb5\xd1\x80\xd1\x82\xd0\xb5\xd0\xbb\xd0\xb5\xd0\xba\xd0\xbe\xd0\xbc'), (95, b'095 ==> Vodafone'), (96, b'096 ==> \xd0\x9a\xd0\xb8\xd0\xb5\xd0\xb2\xd1\x81\xd1\x82\xd0\xb0\xd1\x80'), (97, b'097 ==> \xd0\x9a\xd0\xb8\xd0\xb5\xd0\xb2\xd1\x81\xd1\x82\xd0\xb0\xd1\x80'), (98, b'098 ==> \xd0\x9a\xd0\xb8\xd0\xb5\xd0\xb2\xd1\x81\xd1\x82\xd0\xb0\xd1\x80'), (99, b'099 ==> Vodafone')])),
                ('phone', models.PositiveIntegerField(null=True, verbose_name='\u0422\u0435\u043b\u0435\u0444\u043e\u043d', blank=True)),
                ('code', models.CharField(max_length=32, null=True, verbose_name='USSD Code', blank=True)),
                ('message', models.TextField(null=True, verbose_name='\u0421\u043e\u043e\u0431\u0449\u0435\u043d\u0438\u0435', blank=True)),
                ('message_b64', models.TextField(null=True, verbose_name='\u0421\u043e\u043e\u0431\u0449\u0435\u043d\u0438\u0435 base64', blank=True)),
                ('is_send', models.BooleanField(default=False, verbose_name='\u041e\u0442\u043f\u0440\u0430\u0432\u043b\u0435\u043d\u043e')),
                ('send_at', models.DateTimeField(null=True, verbose_name='\u0414\u0430\u0442\u0430 \u0438 \u0432\u0440\u0435\u043c\u044f \u043e\u0442\u043f\u0440\u0430\u0432\u043a\u0438 USSD', blank=True)),
                ('received_at', models.DateTimeField(null=True, verbose_name='\u0414\u0430\u0442\u0430 \u0438 \u0432\u0440\u0435\u043c\u044f \u043f\u043e\u043b\u0443\u0447\u0435\u043d\u0438\u044f USSD', blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='\u0414\u0430\u0442\u0430 \u0441\u043e\u0437\u0434\u0430\u043d\u0438\u044f', null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='\u0414\u0430\u0442\u0430 \u043e\u0431\u043d\u043e\u0432\u043b\u0435\u043d\u0438\u044f', null=True)),
                ('sim', models.ForeignKey(verbose_name='SIM', blank=True, to='sms_ussd.SIM', null=True)),
                ('user', models.ForeignKey(verbose_name='\u041f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044c', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ['-created_at'],
                'db_table': 'SMS_USSD__USSD',
                'verbose_name': 'USSD',
                'verbose_name_plural': 'USSD',
            },
        ),
    ]
