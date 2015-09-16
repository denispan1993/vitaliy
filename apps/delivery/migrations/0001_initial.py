# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('authModel', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Delivery',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'2015-09-13T12:42:05.148203', max_length=128, null=True, verbose_name='\u0418\u043c\u044f \u0440\u0430\u0441\u0441\u044b\u043b\u043a\u0438', blank=True)),
                ('delivery_test', models.BooleanField(default=True, verbose_name='\u0422\u0435\u0441\u0442\u043e\u0432\u0430\u044f \u0440\u0430\u0441\u0441\u044b\u043b\u043a\u0430')),
                ('type', models.PositiveSmallIntegerField(default=1, verbose_name='\u0422\u0438\u043f \u0440\u0430\u0441\u0441\u044b\u043b\u043a\u0438', choices=[(1, '\u0410\u043a\u0446\u0438\u044f')])),
                ('subject', models.CharField(max_length=256, null=True, verbose_name='Subject \u0440\u0430\u0441\u0441\u044b\u043b\u043a\u0438', blank=True)),
                ('html', models.TextField(default=10, null=True, verbose_name='Html \u0442\u0435\u043a\u0441\u0442 \u0440\u0430\u0441\u0441\u044b\u043b\u043a\u0438', blank=True)),
                ('created_at', models.DateTimeField(default=datetime.datetime(2015, 9, 13, 12, 42, 5, 148461), null=True, verbose_name='\u0414\u0430\u0442\u0430 \u0441\u043e\u0437\u0434\u0430\u043d\u0438\u044f', blank=True)),
                ('updated_at', models.DateTimeField(default=datetime.datetime(2015, 9, 13, 12, 42, 5, 148509), null=True, verbose_name='\u0414\u0430\u0442\u0430 \u043e\u0431\u043d\u043e\u0432\u043b\u0435\u043d\u0438\u044f', blank=True)),
            ],
            options={
                'ordering': ['-created_at'],
                'db_table': 'Delivery',
                'verbose_name': '\u0420\u0430\u0441\u0441\u044b\u043b\u043a\u0430',
                'verbose_name_plural': '\u0420\u0430\u0441\u0441\u044b\u043b\u043a\u0438',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EmailForDelivery',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('send', models.BooleanField(default=False, verbose_name='\u0424\u043b\u0430\u0433 \u043e\u0442\u0441\u044b\u043b\u043a\u0438')),
                ('created_at', models.DateTimeField(default=datetime.datetime(2015, 9, 13, 12, 42, 5, 160386), null=True, verbose_name='\u0414\u0430\u0442\u0430 \u0441\u043e\u0437\u0434\u0430\u043d\u0438\u044f', blank=True)),
                ('updated_at', models.DateTimeField(default=datetime.datetime(2015, 9, 13, 12, 42, 5, 160444), null=True, verbose_name='\u0414\u0430\u0442\u0430 \u043e\u0431\u043d\u043e\u0432\u043b\u0435\u043d\u0438\u044f', blank=True)),
            ],
            options={
                'ordering': ['-created_at'],
                'db_table': 'EmailForDelivery',
                'verbose_name': '\u041c\u043e\u0434\u0435\u043b\u044c \u0420\u0430\u0441\u0441\u044b\u043b\u043a\u0438 (Email \u0430\u0434\u0440\u0435\u0441)',
                'verbose_name_plural': '\u041c\u043e\u0434\u0435\u043b\u0438 \u0420\u0430\u0441\u0441\u044b\u043b\u043e\u043a (Email \u0430\u0434\u0440\u0435\u0441\u0430)',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EmailMiddleDelivery',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('delivery_test', models.BooleanField(default=True, verbose_name='\u0422\u0435\u0441\u0442\u043e\u0432\u0430\u044f \u0440\u0430\u0441\u0441\u044b\u043b\u043a\u0430 - \u043e\u0442\u043e\u0441\u043b\u0430\u043d\u0430')),
                ('created_at', models.DateTimeField(default=datetime.datetime(2015, 9, 13, 12, 42, 5, 149752), null=True, verbose_name='\u0414\u0430\u0442\u0430 \u0441\u043e\u0437\u0434\u0430\u043d\u0438\u044f', blank=True)),
                ('updated_at', models.DateTimeField(default=datetime.datetime(2015, 9, 13, 12, 42, 5, 149799), null=True, verbose_name='\u0414\u0430\u0442\u0430 \u043e\u0431\u043d\u043e\u0432\u043b\u0435\u043d\u0438\u044f', blank=True)),
                ('delivery', models.ForeignKey(verbose_name='\u0423\u043a\u0430\u0437\u0430\u0442\u0435\u043b\u044c \u043d\u0430 \u0440\u0430\u0441\u0441\u044b\u043b\u043a\u0443', to='delivery.Delivery')),
            ],
            options={
                'ordering': ['-created_at'],
                'db_table': 'EmailMiddleDelivery',
                'verbose_name': '\u041f\u0440\u043e\u043c\u0435\u0436\u0443\u0442\u043e\u0447\u043d\u0430\u044f \u043c\u043e\u0436\u0435\u043b\u044c \u0420\u0430\u0441\u0441\u044b\u043b\u043a\u0438',
                'verbose_name_plural': '\u041f\u0440\u043e\u043c\u0435\u0436\u0443\u0442\u043e\u0447\u043d\u044b\u0435 \u043c\u043e\u0436\u0435\u043b\u0438 \u0420\u0430\u0441\u0441\u044b\u043b\u043e\u043a',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='emailfordelivery',
            name='delivery',
            field=models.ForeignKey(verbose_name='\u0423\u043a\u0430\u0437\u0430\u0442\u0435\u043b\u044c \u043d\u0430 \u0440\u0430\u0441\u0441\u044b\u043b\u043a\u0443', to='delivery.EmailMiddleDelivery'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='emailfordelivery',
            name='email',
            field=models.ForeignKey(verbose_name='E-Mail', to='authModel.Email'),
            preserve_default=True,
        ),
    ]
