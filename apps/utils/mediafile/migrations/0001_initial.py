# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import apps.utils.mediafile.models
import compat.ImageWithThumbs.models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MediaFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.PositiveIntegerField(db_index=True)),
                ('serial_number', models.PositiveIntegerField(default=1, verbose_name='\u041f\u043e\u0440\u044f\u0434\u043a\u043e\u0432\u044b \u043d\u043e\u043c\u0435\u0440 \u0444\u0430\u0439\u043b\u0430')),
                ('main', models.NullBooleanField(default=False, verbose_name='\u041f\u0440\u0438\u0437\u043d\u0430\u043a \u0433\u043b\u0430\u0432\u043d\u043e\u0433\u043e \u0444\u0430\u0439\u043b\u0430')),
                ('img', compat.ImageWithThumbs.models.ImageWithThumbsField(null=True, upload_to=apps.utils.mediafile.models.set_path, blank=True)),
                ('title', models.CharField(help_text='title <a> \u0437\u0430\u043f\u0438\u0441\u0438.', max_length=256, null=True, verbose_name='\u0417\u0430\u0433\u043e\u043b\u043e\u0432\u043e\u043a', blank=True)),
                ('name', models.CharField(max_length=256, null=True, verbose_name='\u041d\u0430\u0438\u043c\u0435\u043d\u043e\u0432\u0430\u043d\u0438\u0435', blank=True)),
                ('sign', models.CharField(help_text='\u041f\u043e\u0434\u043f\u0438\u0441\u044c \u043a\u043e\u0442\u043e\u0440\u0430\u044f \u0431\u0443\u0434\u0435 \u043d\u0430\u043f\u0438\u0441\u0430\u043d\u0430 \u043f\u043e\u0434 \u0444\u0430\u0439\u043b\u043e\u043c.', max_length=128, null=True, verbose_name='\u041f\u043e\u0434\u043f\u0438\u0441\u044c sign', blank=True)),
                ('description', models.TextField(null=True, verbose_name='\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435', blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('meta_title', models.CharField(help_text='\u0414\u0430\u043d\u043d\u044b\u0439 title \u0447\u0438\u0442\u0430\u044e\u0442 \u043f\u043e\u0438\u0441\u043a\u043e\u0432\u044b\u0435 \u0441\u0438\u0441\u0442\u0435\u043c\u044b \u0434\u043b\u044f \u043f\u0440\u0430\u0432\u0438\u043b\u044c\u043d\u043e\u0433\u043e \u0440\u0430\u0441\u043f\u043e\u043b\u043e\u0436\u0435\u043d\u0438\u044f \u0444\u0430\u0439\u043b\u0430 \u0432 \u043f\u043e\u0438\u0441\u043a\u0435.', max_length=190, null=True, verbose_name='title', blank=True)),
                ('meta_alt', models.CharField(help_text='\u0414\u0430\u043d\u043d\u044b\u0439 alt \u0447\u0438\u0442\u0430\u044e\u0442 \u043f\u043e\u0438\u0441\u043a\u043e\u0432\u044b\u0435 \u0441\u0438\u0441\u0442\u0435\u043c\u044b \u0434\u043b\u044f \u043f\u0440\u0430\u0432\u0438\u043b\u044c\u043d\u043e\u0433\u043e \u0440\u0430\u0441\u043f\u043e\u043b\u043e\u0436\u0435\u043d\u0438\u044f \u0444\u0430\u0439\u043b\u0430 \u0432 \u043f\u043e\u0438\u0441\u043a\u0435.', max_length=190, null=True, verbose_name='alt', blank=True)),
                ('content_type', models.ForeignKey(related_name='related_MediaFile', to='contenttypes.ContentType')),
            ],
            options={
                'ordering': ['serial_number', '-created_at'],
                'db_table': 'MediaFile',
                'verbose_name': '\u041c\u0435\u0434\u0438\u0430 \u0444\u0430\u0439\u043b',
                'verbose_name_plural': '\u041c\u0435\u0434\u0438\u0430 \u0444\u0430\u0439\u043b\u044b',
            },
            bases=(models.Model,),
        ),
    ]
