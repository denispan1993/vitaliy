# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sms_ussd', '0012_auto_20161228_1544'),
    ]

    operations = [
        migrations.CreateModel(
            name='SIM',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=16, null=True, verbose_name='\u0418\u043c\u044f \u0443\u0441\u0442\u0440\u043e\u0439\u0441\u0442\u0432\u0430', blank=True)),
                ('phone', models.CharField(max_length=14, null=True, verbose_name='\u041d\u043e\u043c\u0435\u0440 \u0442\u0435\u043b\u0435\u0444\u043e\u043d\u0430', blank=True)),
                ('provider', models.CharField(max_length=14, null=True, verbose_name='\u041f\u0440\u043e\u0432\u0430\u0439\u0434\u0435\u0440', blank=True)),
                ('imsi', models.BigIntegerField(unique=True, max_length=15, verbose_name='IMSI')),
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
