# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import compat.FormSlug.models
from django.conf import settings
import datetime


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('product', '0015_category_id_1c'),
    ]

    operations = [
        migrations.CreateModel(
            name='CoordinatorCourse',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('surname', models.CharField(default='\u0424\u0430\u043c\u0438\u043b\u0438\u044f', max_length=128, verbose_name='\u0424\u0430\u043c\u0438\u043b\u0438\u044f')),
                ('name', models.CharField(default='\u0418\u043c\u044f', max_length=128, verbose_name='\u0418\u043c\u044f')),
                ('patronymic', models.CharField(max_length=128, null=True, verbose_name='\u041e\u0442\u0447\u0435\u0441\u0442\u0432\u043e', blank=True)),
                ('url', compat.FormSlug.models.ModelSlugField(db_index=True, max_length=255, null=True, verbose_name='URL \u0430\u0434\u0440\u0435\u0441 \u0412\u0435\u0434\u0443\u0449\u0435\u0433\u043e', blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-created_at'],
                'db_table': 'CalendarCoordinatorCourse',
                'verbose_name': '\u041a\u043e\u043e\u0440\u0434\u0438\u043d\u0430\u0442\u043e\u0440 \u043a\u0443\u0440\u0441\u0430',
                'verbose_name_plural': '\u041a\u043e\u043e\u0440\u0434\u0438\u043d\u0430\u0442\u043e\u0440\u044b \u043a\u0443\u0440\u0441\u043e\u0432',
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sessionid', models.CharField(max_length=32, null=True, verbose_name=b'SessionID', blank=True)),
                ('topic', models.CharField(default=b'', max_length=256, verbose_name='\u0422\u0435\u043c\u0430 \u043a\u0443\u0440\u0441\u0430')),
                ('duration_days', models.PositiveSmallIntegerField(null=True, verbose_name='\u041f\u0440\u043e\u0434\u043e\u043b\u0436\u0438\u0442\u0435\u043b\u044c\u043d\u043e\u0441\u0442\u044c \u0432 \u0434\u043d\u044f\u0445', blank=True)),
                ('duration_hours', models.PositiveSmallIntegerField(null=True, verbose_name='\u041f\u0440\u043e\u0434\u043e\u043b\u0436\u0438\u0442\u0435\u043b\u044c\u043d\u043e\u0441\u0442\u044c \u0432 \u0447\u0430\u0441\u0430\u0445', blank=True)),
                ('description', models.TextField(null=True, verbose_name='\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435 \u0441\u043e\u0431\u044b\u0442\u0438\u044f', blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-created_at'],
                'db_table': 'Calendar',
                'verbose_name': '\u0421\u043e\u0431\u044b\u0442\u0438\u0435',
                'verbose_name_plural': '\u0421\u043e\u0431\u044b\u0442\u0438\u044f',
            },
        ),
        migrations.CreateModel(
            name='LeadingCourse',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('surname', models.CharField(default='\u0424\u0430\u043c\u0438\u043b\u0438\u044f', max_length=128, verbose_name='\u0424\u0430\u043c\u0438\u043b\u0438\u044f')),
                ('name', models.CharField(default='\u0418\u043c\u044f', max_length=128, verbose_name='\u0418\u043c\u044f')),
                ('patronymic', models.CharField(max_length=128, null=True, verbose_name='\u041e\u0442\u0447\u0435\u0441\u0442\u0432\u043e', blank=True)),
                ('url', compat.FormSlug.models.ModelSlugField(db_index=True, max_length=255, null=True, verbose_name='URL \u0430\u0434\u0440\u0435\u0441 \u0412\u0435\u0434\u0443\u0449\u0435\u0433\u043e', blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-created_at'],
                'db_table': 'CalendarLeadingCourse',
                'verbose_name': '\u0412\u0435\u0434\u0443\u0449\u0438\u0439(\u0430\u044f) \u043a\u0443\u0440\u0441\u0430',
                'verbose_name_plural': '\u0412\u0435\u0434\u0443\u0449\u0438\u0435(\u0438\u0438) \u043a\u0443\u0440\u0441\u043e\u0432',
            },
        ),
        migrations.CreateModel(
            name='LocationDate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_start', models.DateField(default=datetime.date.today, verbose_name='\u0414\u0430\u0442\u0430 \u043d\u0430\u0447\u0430\u043b\u0430 \u043c\u0435\u0440\u043e\u043f\u0440\u0438\u044f\u0442\u0438\u044f')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('city', models.ForeignKey(default=1, verbose_name='\u0413\u043e\u0440\u043e\u0434', to='product.City')),
                ('coordinator', models.ForeignKey(default=1, verbose_name='\u041a\u043e\u043e\u0440\u0434\u0438\u043d\u0430\u0442\u043e\u0440 \u043a\u0443\u0440\u0441\u0430', to='mycalendar.CoordinatorCourse')),
            ],
            options={
                'ordering': ['-created_at'],
                'db_table': 'CalendarLocationDate',
                'verbose_name': '\u041c\u0435\u0441\u0442\u043e \u0414\u0430\u0442\u0430 \u0412\u0440\u0435\u043c\u044f',
                'verbose_name_plural': '\u041c\u0435\u0441\u0442\u0430 \u0414\u0430\u0442\u044b \u0412\u0440\u0435\u043c\u044f',
            },
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('section', models.CharField(default=b'', max_length=256, verbose_name='\u0420\u0430\u0437\u0434\u0435\u043b \u043c\u0435\u0440\u043e\u043f\u0440\u0438\u044f\u0442\u0438\u044f')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-created_at'],
                'db_table': 'CalendarSection',
                'verbose_name': '\u0420\u0430\u0437\u0434\u0435\u043b',
                'verbose_name_plural': '\u0420\u0430\u0437\u0434\u0435\u043b\u044b',
            },
        ),
        migrations.AddField(
            model_name='event',
            name='leading_course',
            field=models.ForeignKey(default=1, verbose_name='\u0412\u0435\u0434\u0443\u0449\u0438\u0439(\u0430\u044f) \u043a\u0443\u0440\u0441\u044b', to='mycalendar.LeadingCourse'),
        ),
        migrations.AddField(
            model_name='event',
            name='location_date',
            field=models.ManyToManyField(to='mycalendar.LocationDate', verbose_name='\u0413\u043e\u0440\u043e\u0434 \u0438 \u0432\u0440\u0435\u043c\u044f \u043f\u0440\u043e\u0432\u0435\u0434\u0435\u043d\u0438\u044f'),
        ),
        migrations.AddField(
            model_name='event',
            name='section',
            field=models.ForeignKey(default=1, verbose_name='\u0420\u0430\u0437\u0434\u0435\u043b \u043a\u0443\u0440\u0441\u0430', to='mycalendar.Section'),
        ),
        migrations.AddField(
            model_name='event',
            name='user',
            field=models.ForeignKey(verbose_name='\u041f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044c', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
