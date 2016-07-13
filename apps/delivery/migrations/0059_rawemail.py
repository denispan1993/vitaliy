# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0058_auto_20160713_1732'),
    ]

    operations = [
        migrations.CreateModel(
            name='RawEmail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('from_header', models.CharField(max_length=255, null=True, verbose_name='From header', blank=True)),
                ('to_header', models.TextField(null=True, verbose_name='To header', blank=True)),
                ('raw_email', models.TextField(null=True, verbose_name='Raw Email', blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='\u0414\u0430\u0442\u0430 \u0441\u043e\u0437\u0434\u0430\u043d\u0438\u044f', null=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('account', models.ForeignKey(verbose_name='MailBox', blank=True, to='delivery.MailAccount', null=True)),
            ],
            options={
                'ordering': ['-created_at'],
                'db_table': 'RawEmail',
                'verbose_name': 'Raw\u0415\u043c\u044d\u0439\u043b',
                'verbose_name_plural': 'Raw\u0415\u043c\u044d\u0439\u043b\u044b',
            },
        ),
    ]
