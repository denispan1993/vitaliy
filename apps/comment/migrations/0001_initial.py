# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import mptt.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.PositiveIntegerField(db_index=True, null=True, blank=True)),
                ('serial_number', models.PositiveSmallIntegerField(default=1, null=True, verbose_name='\u041f\u043e\u0440\u044f\u0434\u043e\u043a \u0441\u043e\u0440\u0442\u0438\u0440\u043e\u0432\u043a\u0438', blank=True)),
                ('is_active', models.BooleanField(default=True, help_text='\u0415\u0441\u043b\u0438 \u043c\u044b \u0445\u043e\u0442\u0438\u043c \u0447\u0442\u043e\u0431\u044b \u043a\u043e\u043c\u043c\u0435\u043d\u0442\u0430\u0440\u0438\u0439 \u043d\u0435 \u043f\u043e\u043a\u0430\u0437\u044b\u0432\u0430\u043b\u0441\u044f, \u0441\u0442\u0430\u0432\u0438\u043c \u0434\u0430\u043d\u043d\u043e\u0435 \u043f\u043e\u043b\u0435 \u0432 False.', verbose_name='\u0410\u043a\u0442\u0438\u0432. \u0438\u043b\u0438 \u041f\u0430\u0441\u0438\u0432.')),
                ('shown_colored', models.BooleanField(default=False, help_text='\u0415\u0441\u043b\u0438 \u043c\u044b \u0445\u043e\u0442\u0438\u043c \u0447\u0442\u043e\u0431\u044b \u043a\u043e\u043c\u043c\u0435\u043d\u0442\u0430\u0440\u0438\u0439 \u0431\u044b\u043b \u0432\u044b\u0434\u0435\u043b\u0435\u043d \u0446\u0432\u0435\u0442\u043e\u043c \u0424\u0443\u043a\u0441\u0438\u044f, \u0441\u0442\u0430\u0432\u0438\u043c \u0434\u0430\u043d\u043d\u043e\u0435 \u043f\u043e\u043b\u0435 \u0432 True.', verbose_name='\u0412\u044b\u0434\u0435\u043b\u0438\u0442\u044c \u0446\u0432\u0435\u0442\u043e\u043c')),
                ('shown_bold', models.BooleanField(default=False, help_text='\u0415\u0441\u043b\u0438 \u043c\u044b \u0445\u043e\u0442\u0438\u043c \u0447\u0442\u043e\u0431\u044b \u043a\u043e\u043c\u043c\u0435\u043d\u0442\u0430\u0440\u0438\u0439 \u0431\u044b\u043b \u0432\u044b\u0434\u0435\u043b\u0435\u043d \u0436\u0438\u0440\u043d\u044b\u043c \u0448\u0440\u0438\u0444\u0442\u043e\u043c, \u0441\u0442\u0430\u0432\u0438\u043c \u0434\u0430\u043d\u043d\u043e\u0435 \u043f\u043e\u043b\u0435 \u0432 True.', verbose_name='\u0412\u044b\u0434\u0435\u043b\u0438\u0442\u044c \u0436\u0438\u0440\u043d\u044b\u043c')),
                ('shown_italic', models.BooleanField(default=False, help_text='\u0415\u0441\u043b\u0438 \u043c\u044b \u0445\u043e\u0442\u0438\u043c \u0447\u0442\u043e\u0431\u044b \u043a\u043e\u043c\u043c\u0435\u043d\u0442\u0430\u0440\u0438\u0439 \u0431\u044b\u043b \u0432\u044b\u0434\u0435\u043b\u0435\u043d \u043d\u0430\u043a\u043b\u043e\u043d\u043d\u044b\u043c \u0448\u0440\u0438\u0444\u0442\u043e\u043c, \u0441\u0442\u0430\u0432\u0438\u043c \u0434\u0430\u043d\u043d\u043e\u0435 \u043f\u043e\u043b\u0435 \u0432 True.', verbose_name='\u0412\u044b\u0434\u0435\u043b\u0438\u0442\u044c \u043a\u0443\u0440\u0441\u0438\u0432\u043e\u043c')),
                ('font_px', models.PositiveSmallIntegerField(default=14, help_text='\u0420\u0430\u0437\u043c\u0435\u0440 \u0448\u0440\u0438\u0444\u0442\u0430 \u043a\u043e\u043c\u043c\u0435\u043d\u0442\u0430\u0440\u0438\u044f \u0432 \u043f\u0438\u043a\u0441\u0435\u043b\u044f\u0445,', verbose_name='\u0420\u0430\u0437\u043c\u0435\u0440 \u0448\u0440\u0438\u0444\u0442\u0430')),
                ('name', models.CharField(default=None, help_text='\u041a\u0430\u043a \u0447\u0435\u043b\u043e\u0432\u0435\u043a \u043f\u0440\u0435\u0434\u0441\u0442\u0430\u0432\u0438\u043b\u0441\u044f, \u0438\u043c\u044f \u043a\u043e\u0442\u043e\u0440\u043e\u0435 \u0431\u0443\u0434\u0435\u0442 \u0432\u044b\u0432\u043e\u0434\u0438\u0442\u0441\u044f \u043d\u0430 \u0441\u0430\u0439\u0442\u0435.', max_length=64, verbose_name='\u0418\u043c\u044f')),
                ('sessionid', models.CharField(max_length=32, null=True, verbose_name='SessionID', blank=True)),
                ('comment', models.TextField(verbose_name='\u041a\u043e\u043c\u043c\u0435\u043d\u0442\u0430\u0440\u0438\u0439')),
                ('rating', models.SmallIntegerField(null=True, verbose_name='\u0420\u0435\u0439\u0442\u0438\u043d\u0433', blank=True)),
                ('pass_moderation', models.BooleanField(default=False, help_text='\u0415\u0441\u043b\u0438 \u0441\u0442\u043e\u0438\u0442 \u0433\u0430\u043b\u043e\u0447\u043a\u0430, \u0442\u043e \u043a\u043e\u043c\u043c\u0435\u043d\u0442\u0430\u0440\u0438\u0439 \u043f\u0440\u043e\u0448\u0435\u043b \u043c\u043e\u0434\u0435\u0440\u0430\u0446\u0438\u044e.', verbose_name='\u0424\u043b\u0430\u0433 \u043c\u043e\u0434\u0435\u0440\u0430\u0446\u0438\u0438')),
                ('require_a_response', models.BooleanField(default=False, help_text='\u041f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044c \u0437\u0430\u043f\u0440\u043e\u0441\u0438\u043b \u043e\u0442\u0432\u0435\u0442 \u043d\u0430 \u0441\u0432\u043e\u0439 \u043a\u043e\u043c\u043c\u0435\u043d\u0442\u0430\u0440\u0438\u0439.', verbose_name='\u0417\u0430\u043f\u0440\u043e\u0441 \u043e\u0442\u0432\u0435\u0442\u0430')),
                ('email_for_response', models.CharField(default=None, max_length=64, blank=True, help_text='E-Mail \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044f \u043d\u0430 \u043a\u043e\u0442\u043e\u0440\u044b\u0439 \u043d\u0443\u0436\u043d\u043e \u043e\u0442\u043e\u0441\u043b\u0430\u0442\u044c \u0441\u0441\u044b\u043b\u043a\u0443 \u043d\u0430 \u043e\u0442\u0432\u0435\u0442 \u043d\u0430 \u043a\u043e\u043c\u043c\u0435\u043d\u0442\u0430\u0440\u0438\u0439.', null=True, verbose_name='E-Mail \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044f')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('mptt_level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('comment_parent', mptt.fields.TreeForeignKey(related_name='children', verbose_name='\u041a\u043e\u043c\u043c\u0435\u043d\u0442\u0430\u0440\u0438\u0439 \u043d\u0430 \u043a\u043e\u0442\u043e\u0440\u044b\u0439 \u043e\u0442\u0432\u0435\u0447\u0430\u0435\u0442 \u044d\u0442\u043e\u0442 \u043a\u043e\u043c\u043c\u0435\u043d\u0442\u0430\u0440\u0438\u0439', blank=True, to='comment.Comment', null=True)),
                ('content_type', models.ForeignKey(related_name='related_Product', blank=True, to='contenttypes.ContentType', null=True)),
                ('user', models.ForeignKey(verbose_name='\u041f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044c', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ['-created_at'],
                'db_table': 'Comment',
                'verbose_name': '\u041a\u043e\u043c\u043c\u0435\u043d\u0442\u0430\u0440\u0438\u0439',
                'verbose_name_plural': '\u041a\u043e\u043c\u043c\u0435\u043d\u0442\u0430\u0440\u0438\u0438',
            },
        ),
    ]
