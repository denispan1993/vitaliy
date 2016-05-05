# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0008_auto_20151202_0847'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mycalendar', '0007_auto_20151202_0835'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sessionid', models.CharField(max_length=32, null=True, verbose_name='SessionID', blank=True)),
                ('title', models.CharField(default='\u0421\u043e\u0431\u044b\u0442\u0438\u0435', max_length=256, verbose_name='\u041d\u0430\u0438\u043c\u0435\u043d\u043e\u0432\u0430\u043d\u0438\u0435')),
                ('description', models.TextField(null=True, verbose_name='\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435 \u0441\u043e\u0431\u044b\u0442\u0438\u044f', blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-created_at'],
                'db_table': 'Calendar',
                'verbose_name': '\u0421\u043e\u0431\u0438\u0442\u0438\u0435',
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
            name='LocationDateTime',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_start', models.DateField(default=datetime.date.today, verbose_name='\u0414\u0430\u0442\u0430 \u043d\u0430\u0447\u0430\u043b\u0430 \u043c\u0435\u0440\u043e\u043f\u0440\u0438\u044f\u0442\u0438\u044f')),
                ('date_end', models.DateField(default=datetime.date.today, verbose_name='\u0414\u0430\u0442\u0430 \u043e\u043a\u043e\u043d\u0447\u0430\u043d\u0438\u044f \u043c\u0435\u0440\u043e\u043f\u0440\u0438\u044f\u0442\u0438\u044f')),
                ('time_start', models.TimeField(default=django.utils.timezone.now, verbose_name='\u0412\u0440\u0435\u043c\u044f \u043d\u0430\u0447\u0430\u043b\u0430 \u043c\u0435\u0440\u043e\u043f\u0440\u0438\u044f\u0442\u0438\u044f')),
                ('time_end', models.TimeField(default=django.utils.timezone.now, verbose_name='\u0412\u0440\u0435\u043c\u044f \u043e\u043a\u043e\u043d\u0447\u0430\u043d\u0438\u044f \u043c\u0435\u0440\u043e\u043f\u0440\u0438\u044f\u0442\u0438\u044f')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('city', models.ForeignKey(default=1, verbose_name='\u0413\u043e\u0440\u043e\u0434', to='product.City')),
            ],
            options={
                'ordering': ['-created_at'],
                'db_table': 'CalendarLocationDateTime',
                'verbose_name': '\u041c\u0435\u0441\u0442\u043e \u0414\u0430\u0442\u0430 \u0412\u0440\u0435\u043c\u044f',
                'verbose_name_plural': '\u041c\u0435\u0441\u0442\u0430 \u0414\u0430\u0442\u044b \u0412\u0440\u0435\u043c\u044f',
            },
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('subject', models.CharField(default='\u0422\u0435\u043c\u0430 \u043c\u0435\u0440\u043e\u043f\u0440\u0438\u044f\u0442\u0438\u044f', max_length=256, verbose_name='\u0422\u0435\u043c\u0430 \u043c\u0435\u0440\u043e\u043f\u0440\u0438\u044f\u0442\u0438\u044f')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-created_at'],
                'db_table': 'CalendarSubject',
                'verbose_name': '\u0422\u0435\u043c\u0430',
                'verbose_name_plural': '\u0422\u0435\u043c\u044b',
            },
        ),
        migrations.AddField(
            model_name='event',
            name='leading_course',
            field=models.ForeignKey(default=1, verbose_name='\u0412\u0435\u0434\u0443\u0449\u0438\u0439(\u0430\u044f) \u043a\u0443\u0440\u0441\u044b', to='mycalendar.LeadingCourse'),
        ),
        migrations.AddField(
            model_name='event',
            name='location_date_time',
            field=models.ManyToManyField(default=1, to='mycalendar.LocationDateTime', verbose_name='\u041c\u0435\u0441\u0442\u043e \u0434\u0430\u0442\u0430 \u0438 \u0432\u0440\u0435\u043c\u044f \u043f\u0440\u043e\u0432\u0435\u0434\u0435\u043d\u0438\u044f'),
        ),
        migrations.AddField(
            model_name='event',
            name='subject',
            field=models.ForeignKey(default=1, verbose_name='\u0422\u0435\u043c\u0430 \u043a\u0443\u0440\u0441\u0430', to='mycalendar.Subject'),
        ),
        migrations.AddField(
            model_name='event',
            name='user',
            field=models.ForeignKey(verbose_name='\u041f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044c', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
