# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sms_ussd', '0009_sms_message_b64'),
    ]

    operations = [
        migrations.CreateModel(
            name='USSD',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('direction', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='\u041d\u0430\u043f\u0440\u0430\u0432\u043b\u0435\u043d\u0438\u0435', choices=[(1, b'Send'), (2, b'Receive')])),
                ('from_device', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='\u0421 \u043a\u0430\u043a\u043e\u0433\u043e \u043d\u043e\u043c\u0435\u0440\u0430 \u0442\u0435\u043b\u0435\u0444\u043e\u043d\u0430', choices=[(1, b'Vodafone1 +380(66)467-12-90')])),
                ('sessionid', models.CharField(max_length=32, null=True, verbose_name='SessionID', blank=True)),
                ('task_id', models.CharField(max_length=255, null=True, verbose_name='task.id', blank=True)),
                ('code', models.CharField(max_length=32, null=True, verbose_name='USSD Code', blank=True)),
                ('message', models.TextField(null=True, verbose_name='\u0421\u043e\u043e\u0431\u0449\u0435\u043d\u0438\u0435', blank=True)),
                ('message_b64', models.TextField(null=True, verbose_name='\u0421\u043e\u043e\u0431\u0449\u0435\u043d\u0438\u0435 base64', blank=True)),
                ('is_send', models.BooleanField(default=False, verbose_name='\u041e\u0442\u043f\u0440\u0430\u0432\u043b\u0435\u043d\u043e')),
                ('send_at', models.DateTimeField(null=True, verbose_name='\u0414\u0430\u0442\u0430 \u0438 \u0432\u0440\u0435\u043c\u044f \u043e\u0442\u043f\u0440\u0430\u0432\u043a\u0438 USSD', blank=True)),
                ('received_at', models.DateTimeField(null=True, verbose_name='\u0414\u0430\u0442\u0430 \u0438 \u0432\u0440\u0435\u043c\u044f \u043f\u043e\u043b\u0443\u0447\u0435\u043d\u0438\u044f USSD', blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='\u0414\u0430\u0442\u0430 \u0441\u043e\u0437\u0434\u0430\u043d\u0438\u044f', null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='\u0414\u0430\u0442\u0430 \u043e\u0431\u043d\u043e\u0432\u043b\u0435\u043d\u0438\u044f', null=True)),
                ('user', models.ForeignKey(verbose_name='\u041f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044c', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ['-created_at'],
                'db_table': 'SMS_USSD__USSD',
                'verbose_name': 'USSD',
                'verbose_name_plural': 'USSD',
            },
        ),
        migrations.AlterField(
            model_name='sms',
            name='from_phone_char',
            field=models.CharField(max_length=64, null=True, verbose_name='\u041d\u043e\u043c\u0435\u0440 \u0442\u0435\u043b\u0435\u0444\u043e\u043d\u0430 (\u041e\u0442\u043a\u0443\u0434\u0430)', blank=True),
        ),
        migrations.AlterField(
            model_name='sms',
            name='to_phone_char',
            field=models.CharField(max_length=64, null=True, verbose_name='\u041d\u043e\u043c\u0435\u0440 \u0442\u0435\u043b\u0435\u0444\u043e\u043d\u0430 (\u041a\u0443\u0434\u0430)', blank=True),
        ),
    ]
