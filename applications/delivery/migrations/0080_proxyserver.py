# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0079_traceofvisits_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProxyServer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('from_whence', models.PositiveSmallIntegerField(verbose_name='\u041e\u0442\u043a\u0443\u0434\u0430', choices=[(1, 'http://hideme.ru')])),
                ('host', models.CharField(default='000.000.000.000', max_length=15, verbose_name='Host')),
                ('port', models.PositiveIntegerField(default=1080, verbose_name='Port')),
                ('http', models.BooleanField(default=False, verbose_name='HTTP')),
                ('https', models.BooleanField(default=False, verbose_name='HTTPS')),
                ('sock4', models.BooleanField(default=False, verbose_name='SOCK4')),
                ('sock5', models.BooleanField(default=False, verbose_name='SOCK5')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='\u0414\u0430\u0442\u0430 \u0441\u043e\u0437\u0434\u0430\u043d\u0438\u044f', null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='\u0414\u0430\u0442\u0430 \u043e\u0431\u043d\u043e\u0432\u043b\u0435\u043d\u0438\u044f', null=True)),
            ],
            options={
                'ordering': ['-created_at'],
                'db_table': 'Delivery_ProxyServer',
                'verbose_name': 'ProxyServer',
                'verbose_name_plural': 'ProxyServers',
            },
        ),
    ]
