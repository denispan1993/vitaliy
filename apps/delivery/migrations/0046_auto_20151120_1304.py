# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import apps.delivery.models
import datetime
import compat.ImageWithThumbs.models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('delivery', '0045_auto_20151120_1301'),
    ]

    operations = [
        migrations.CreateModel(
            name='Email_Img',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.PositiveIntegerField(db_index=True)),
                ('name', models.CharField(max_length=256, null=True, verbose_name='\u041d\u0430\u0438\u043c\u0435\u043d\u043e\u0432\u0430\u043d\u0438\u0435 \u043a\u0430\u0440\u0442\u0438\u043d\u043a\u0438', blank=True)),
                ('tag_name', models.CharField(help_text='TAG \u043a\u0430\u0440\u0442\u0438\u043d\u043a\u0438 \u043d\u0435 \u043c\u043e\u0436\u0435\u0442 \u0431\u044b\u0442\u044c \u0434\u043b\u0438\u043d\u0435\u0435 8 \u0441\u0438\u043c\u0432\u043e\u043b\u043e\u0432, \u0442\u043e\u043b\u044c\u043a\u043e \u0430\u043d\u0433\u043b\u0438\u0439\u0441\u043a\u0438\u0435 \u043c\u0430\u043b\u0435\u043d\u044c\u043a\u0438\u0435 \u0431\u0443\u043a\u0432\u044b \u0438 \u0446\u0438\u0444\u0440\u044b \u0431\u0435\u0437 \u043f\u0440\u043e\u0431\u0435\u043b\u043e\u0432 \u0438 \u043f\u043e\u0434\u0447\u0435\u0440\u043a\u0438\u0432\u0430\u043d\u0438\u0439', max_length=8, null=True, verbose_name="\u0418\u043c\u044f tag'a \u043a\u0430\u0440\u0442\u0438\u043d\u043a\u0438", blank=True)),
                ('image', compat.ImageWithThumbs.models.ImageWithThumbsField(upload_to=apps.delivery.models.set_path_img)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('content_type', models.ForeignKey(related_name='related_Email_Img', to='contenttypes.ContentType')),
            ],
            options={
                'ordering': ['-created_at'],
                'db_table': 'EMail_Img',
                'verbose_name': '\u041a\u0430\u0440\u0442\u0438\u043d\u043a\u0430 \u0434\u043b\u044f E-Mail',
                'verbose_name_plural': '\u041a\u0430\u0440\u0442\u0438\u043d\u043a\u0438\u0438 \u0434\u043b\u044f E-Mail',
            },
        ),
        migrations.AlterField(
            model_name='delivery',
            name='name',
            field=models.CharField(default=b'2015-11-20T13:04:50.830821', max_length=128, null=True, verbose_name='\u0418\u043c\u044f \u0440\u0430\u0441\u0441\u044b\u043b\u043a\u0438', blank=True),
        ),
        migrations.AlterField(
            model_name='mailaccount',
            name='auto_active_datetime',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 20, 13, 4, 50, 825134), verbose_name='\u0414\u0430\u0442\u0430 \u0437\u0430\u043a\u0440\u044b\u0442\u0438\u044f \u0430\u043a\u043a\u0430\u0443\u043d\u0442\u0430'),
        ),
    ]
