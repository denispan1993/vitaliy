# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import applications.utils.captcha.views
import applications.utils.captcha.models
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Captcha_Images',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image_type', models.PositiveSmallIntegerField(default=1, verbose_name='\u0422\u0438\u043f \u043a\u0430\u0440\u0442\u0438\u043d\u043a\u0438', choices=[(1, '\u0426\u0432\u0435\u0442\u044b'), (3, '\u041b\u0435\u0433\u043a\u043e\u0432\u044b\u0435 \u043c\u0430\u0448\u0438\u043d\u044b'), (9, '\u0414\u043e\u043c\u0430')])),
                ('image', models.ImageField(upload_to=applications.utils.captcha.models.set_path_photo, verbose_name='\u041a\u0430\u0440\u0442\u0438\u043d\u043a\u0430')),
                ('alt', models.CharField(max_length=64, verbose_name='Alt \u043a\u0430\u0440\u0442\u0438\u043d\u043a\u0438')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-created_at'],
                'db_table': 'Captcha_Images',
                'verbose_name': 'Captcha \u043a\u0430\u0440\u0442\u0438\u043d\u043a\u0430',
                'verbose_name_plural': 'Captcha \u043a\u0430\u0440\u0442\u0438\u043d\u043a\u0438',
            },
        ),
        migrations.CreateModel(
            name='Captcha_Key',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(default=applications.utils.captcha.views.key_generator, unique=True, max_length=8, verbose_name='\u041a\u0430\u043f\u0447\u0430 \u043a\u043e\u0434')),
                ('image_type', models.PositiveSmallIntegerField(default=0, verbose_name='\u0422\u0438\u043f \u043a\u0430\u0440\u0442\u0438\u043d\u043a\u0438')),
                ('next_use', models.DateTimeField(default=datetime.datetime(2016, 5, 5, 21, 44, 40, 871366))),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('image', models.ForeignKey(verbose_name='\u0421\u0441\u044b\u043b\u043a\u0430 \u043d\u0430 \u043a\u0430\u0440\u0442\u0438\u043d\u043a\u0443', to='captcha.Captcha_Images')),
            ],
            options={
                'ordering': ['-created_at'],
                'db_table': 'Captcha_Keys',
                'verbose_name': 'Captcha \u041a\u043b\u044e\u0447',
                'verbose_name_plural': 'Captchas \u041a\u043b\u044e\u0447\u0438',
            },
        ),
    ]
