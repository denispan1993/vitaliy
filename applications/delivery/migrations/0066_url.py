# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0065_remove_delivery_subject'),
    ]

    operations = [
        migrations.CreateModel(
            name='Url',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url_id', models.PositiveSmallIntegerField(default=1, verbose_name='Url ID')),
                ('href', models.CharField(default=b'http://keksik.com.ua/', max_length=256, verbose_name='URL')),
                ('str', models.CharField(default=b'http://keksik.com.ua/', max_length=256, verbose_name='\u0421\u0442\u0440\u043e\u043a\u0430')),
                ('title', models.CharField(default=b'http://keksik.com.ua/', max_length=256, verbose_name='Title')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='\u0414\u0430\u0442\u0430 \u0441\u043e\u0437\u0434\u0430\u043d\u0438\u044f', null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='\u0414\u0430\u0442\u0430 \u043e\u0431\u043d\u043e\u0432\u043b\u0435\u043d\u0438\u044f', null=True)),
                ('delivery', models.ForeignKey(verbose_name='\u0420\u0430\u0441\u0441\u044b\u043b\u043a\u0430', to='delivery.Delivery')),
            ],
            options={
                'ordering': ['-created_at'],
                'db_table': 'Url',
                'verbose_name': 'Url',
                'verbose_name_plural': 'Urls',
            },
        ),
    ]
