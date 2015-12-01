# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import compat.FormSlug.models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name_ru', models.CharField(max_length=64, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 \u0433\u043e\u0440\u043e\u0434\u0430 Russian')),
                ('name_en', models.CharField(max_length=50, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 \u0433\u043e\u0440\u043e\u0434\u0430 English')),
                ('phone_code', models.PositiveIntegerField(null=True, verbose_name='\u0422\u0435\u043b\u0435\u0444\u043e\u043d\u043d\u044b\u0439 \u043a\u043e\u0434 \u0433\u043e\u0440\u043e\u0434\u0430', blank=True)),
                ('url', compat.FormSlug.models.ModelSlugField(db_index=True, max_length=255, null=True, verbose_name='URL \u0430\u0434\u0440\u0435\u0441 \u0441\u0442\u0440\u0430\u043d\u044b', blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['id'],
                'db_table': 'City',
                'verbose_name': '\u0413\u043e\u0440\u043e\u0434',
                'verbose_name_plural': '\u0413\u043e\u0440\u043e\u0434\u0430',
            },
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name_ru', models.CharField(max_length=64, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 \u043e\u0431\u043b\u0430\u0441\u0442\u0438 Russian')),
                ('name_en', models.CharField(max_length=50, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 \u043e\u0431\u043b\u0430\u0441\u0442\u0438 English')),
                ('url', compat.FormSlug.models.ModelSlugField(db_index=True, max_length=255, null=True, verbose_name='URL \u0430\u0434\u0440\u0435\u0441 \u0441\u0442\u0440\u0430\u043d\u044b', blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('country', models.ForeignKey(default=1, verbose_name='\u0421\u0442\u0440\u0430\u043d\u0430', to='product.Country')),
            ],
            options={
                'ordering': ['id'],
                'db_table': 'Region',
                'verbose_name': '\u041e\u0431\u043b\u0430\u0441\u0442\u044c',
                'verbose_name_plural': '\u041e\u0431\u043b\u0430\u0441\u0442\u0438',
            },
        ),
        migrations.AlterField(
            model_name='viewed',
            name='last_viewed',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 1, 11, 39, 36, 442666), verbose_name='\u0414\u0430\u0442\u0430 \u043f\u043e\u0441\u043b\u0435\u0434\u043d\u0435\u0433\u043e \u043f\u0440\u043e\u0441\u043c\u043e\u0442\u0440\u0430'),
        ),
        migrations.AddField(
            model_name='city',
            name='region',
            field=models.ForeignKey(default=1, verbose_name='\u041e\u0431\u043b\u0430\u0441\u0442\u044c', to='product.Region'),
        ),
    ]
