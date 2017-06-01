# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Action',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default='\u0410\u043a\u0446\u0438\u044f \u043e\u0442 2015-11-13 16:04:19.081540', max_length=256, verbose_name='\u041d\u0430\u0438\u043c\u0435\u043d\u043e\u0432\u0430\u043d\u0438\u0435 \u0430\u043a\u0446\u0438\u0438')),
                ('datetime_start', models.DateTimeField(default=datetime.datetime(2015, 11, 13, 16, 4, 19, 81586), verbose_name='\u0414\u0430\u0442\u0430 \u043d\u0430\u0447\u0430\u043b\u0430 \u0430\u043a\u0446\u0438\u0438')),
                ('datetime_end', models.DateTimeField(default=datetime.datetime(2015, 11, 20, 16, 4, 19, 81613), verbose_name='\u0414\u0430\u0442\u0430 \u043e\u043a\u043e\u043d\u0447\u0430\u043d\u0438\u044f \u0430\u043a\u0446\u0438\u0438')),
                ('auto_start', models.BooleanField(default=True, verbose_name='\u0410\u0432\u0442\u043e \u0441\u0442\u0430\u0440\u0442')),
                ('auto_end', models.BooleanField(default=True, verbose_name='\u0410\u0432\u0442\u043e \u0441\u0442\u043e\u043f')),
                ('auto_del', models.BooleanField(default=False, verbose_name='\u0410\u0432\u0442\u043e \u0443\u0434\u0430\u043b\u0435\u043d\u0438\u0435 \u0430\u043a\u0446\u0438\u0438')),
                ('deleted', models.BooleanField(default=False, verbose_name='\u0423\u0434\u0430\u043b\u0435\u043d\u043d\u0430\u044f \u0430\u043a\u0446\u0438\u044f')),
                ('auto_del_action_from_product', models.BooleanField(default=False, verbose_name='\u0423\u0434\u0430\u043b\u0435\u043d\u0438\u0435 \u0430\u043a\u0446\u0438\u0438 \u0438\u0437 \u0442\u043e\u0432\u0430\u0440\u0430')),
                ('auto_del_action_price', models.BooleanField(default=True, verbose_name='\u0410\u0432\u0442\u043e \u0443\u0434\u0430\u043b\u0435\u043d\u0438\u0435 \u0430\u043a\u0446\u0438\u043e\u043d\u043d\u043e\u0439 \u0446\u0435\u043d\u044b')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-created_at'],
                'db_table': 'Action',
                'verbose_name': '\u0410\u043a\u0446\u0438\u044f',
                'verbose_name_plural': '\u0410\u043a\u0446\u0438\u0438',
            },
        ),
    ]
