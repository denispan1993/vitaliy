# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CallBack',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sessionid', models.CharField(max_length=32, null=True, verbose_name='SessionID', blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=64, null=True, verbose_name='\u0418\u043c\u044f \u043e\u0441\u0442\u0430\u0432\u0438\u0432\u0448\u0435\u0433\u043e \u043f\u0440\u043e\u0441\u044c\u0431\u0443 "\u043e\u0431\u0440\u0430\u0442\u043d\u044b\u0439 \u0437\u0432\u043e\u043d\u043e\u043a"', blank=True)),
                ('phone', models.CharField(default=b'phone number', max_length=32, verbose_name='\u041d\u043e\u043c\u0435\u0440 \u0442\u0435\u043b\u0435\u0444\u043e\u043d\u0430')),
                ('email', models.EmailField(max_length=254, null=True, verbose_name='E-Mail', blank=True)),
                ('user', models.ForeignKey(verbose_name='\u041f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044c', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ['-created_at'],
                'db_table': 'CallBack',
                'verbose_name': '\u041e\u0431\u0440\u0430\u0442\u043d\u044b\u0439 \u0437\u0432\u043e\u043d\u043e\u043a',
                'verbose_name_plural': '\u041e\u0431\u0440\u0430\u0442\u043d\u044b\u0435 \u0437\u0432\u043e\u043d\u043a\u0438',
            },
        ),
    ]
