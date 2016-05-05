# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import apps.slide.models
import compat.ImageWithThumbs.models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Slide',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default='\u0421\u043b\u0430\u0439\u0434 \u043e\u0442 2016-05-05 21:46:46.033444', max_length=128, null=True, verbose_name='\u041d\u0430\u0438\u043c\u0435\u043d\u043e\u0432\u0430\u043d\u0438\u0435 \u0441\u043b\u0430\u0439\u0434\u0430', blank=True)),
                ('order', models.PositiveSmallIntegerField(null=True, blank=True, help_text='\u0426\u0438\u0444\u0440\u044b \u043e\u0442 1 \u0434\u043e 99', unique=True, verbose_name='\u041f\u043e\u0440\u044f\u0434\u043e\u043a \u0441\u043e\u0440\u0442\u0438\u0440\u043e\u0432\u043a\u0438', db_index=True)),
                ('is_active', models.BooleanField(default=True, help_text='\u0415\u0441\u043b\u0438 \u043c\u044b \u0445\u043e\u0442\u0438\u043c \u0447\u0442\u043e\u0431\u044b \u0441\u043b\u0430\u0439\u0434 \u043d\u0435 \u043f\u043e\u043a\u0430\u0437\u044b\u0432\u0430\u043b\u0441\u044f, \u0441\u0442\u0430\u0432\u0438\u043c \u0434\u0430\u043d\u043d\u043e\u0435 \u043f\u043e\u043b\u0435 \u0432 False.', verbose_name='\u0410\u043a\u0442\u0438\u0432. \u0438\u043b\u0438 \u041f\u0430\u0441\u0438\u0432')),
                ('object_id', models.PositiveIntegerField(db_index=True, null=True, blank=True)),
                ('title', models.CharField(default='title', max_length=255, blank=True, help_text='\u0412\u0435\u0440\u0445\u043d\u044f\u044f \u0441\u0442\u0440\u043e\u0447\u043a\u0430 \u0432 \u043e\u043f\u0438\u0441\u0430\u043d\u0438\u0438 \u0441\u043b\u0430\u0439\u0434\u0430', null=True, verbose_name='title \u0441\u043b\u0430\u0439\u0434\u0430')),
                ('alt', models.CharField(help_text='\u0421\u0442\u0440\u043e\u0447\u043a\u0430 \u043e\u043f\u0438\u0441\u0430\u043d\u0438\u044f \u0441\u043b\u0430\u0439\u0434\u0430 \u0434\u043b\u044f \u043f\u043e\u0438\u0441\u043a\u043e\u0432\u044b\u0445 \u0441\u0438\u0441\u0442\u0435\u043c', max_length=255, null=True, verbose_name='alt \u0441\u043b\u0430\u0439\u0434\u0430', blank=True)),
                ('text', models.CharField(help_text='\u041d\u0438\u0436\u043d\u044f\u044f \u0441\u0442\u0440\u043e\u0447\u043a\u0430 \u0432 \u043e\u043f\u0438\u0441\u0430\u043d\u0438\u0438 \u0441\u043b\u0430\u0439\u0434\u0430', max_length=255, null=True, verbose_name='a \u0441\u043b\u0430\u0439\u0434\u0430', blank=True)),
                ('slide', compat.ImageWithThumbs.models.ImageWithThumbsField(help_text='\u0421\u043b\u0430\u0439\u0434 \u0434\u043e\u043b\u0436\u0435\u043d \u0431\u044b\u0442\u044c \u0432 \u0440\u0430\u0437\u0440\u0435\u0448\u0435\u043d\u0438\u0438 960x360', upload_to=apps.slide.models.set_path_photo)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('content_type', models.ForeignKey(related_name='related_Slide', blank=True, to='contenttypes.ContentType', null=True)),
            ],
            options={
                'ordering': ['order'],
                'db_table': 'Slide',
                'verbose_name': '\u0421\u043b\u0430\u0439\u0434',
                'verbose_name_plural': '\u0421\u043b\u0430\u0439\u0434\u044b',
            },
        ),
    ]
