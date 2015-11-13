# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('product', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sessionid', models.CharField(max_length=32, null=True, verbose_name='SessionID', blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(verbose_name='\u041f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044c', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ['-created_at'],
                'db_table': 'Cart',
                'verbose_name': '\u041a\u043e\u0440\u0437\u0438\u043d\u0430',
                'verbose_name_plural': '\u041a\u043e\u0440\u0437\u0438\u043d\u044b',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DeliveryCompany',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order_number', models.PositiveSmallIntegerField(default=1, null=True, verbose_name='\u041f\u043e\u0440\u044f\u0434\u043e\u043a \u0441\u043e\u0440\u0442\u0438\u0440\u043e\u0432\u043a\u0438', blank=True)),
                ('select_number', models.PositiveSmallIntegerField(default=1, null=True, verbose_name='\u041d\u043e\u043c\u0435\u0440 \u0432 \u0432\u044b\u0432\u043e\u0434\u0435', blank=True)),
                ('name', models.CharField(max_length=64, null=True, verbose_name='\u0418\u043c\u044f \u043a\u043e\u043c\u043f\u0430\u043d\u0438\u0438', blank=True)),
                ('select_string_ru', models.CharField(max_length=64, null=True, verbose_name='\u0421\u0442\u0440\u043e\u043a\u0430 \u0432 \u0432\u044b\u0432\u043e\u0434\u0435', blank=True)),
                ('description', models.TextField(null=True, verbose_name='\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435 \u043a\u043e\u043c\u043f\u0430\u043d\u0438\u0438', blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-created_at'],
                'db_table': 'DeliveryCompany',
                'verbose_name': '\u041a\u043e\u043c\u043f\u0430\u043d\u0438\u0438 \u0434\u043e\u0441\u0442\u0430\u0432\u0449\u0438\u043a\u0438',
                'verbose_name_plural': '\u041a\u043e\u043c\u043f\u0430\u043d\u0438\u044f \u0434\u043e\u0441\u0442\u0430\u0432\u0449\u0438\u043a',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sessionid', models.CharField(max_length=32, null=True, verbose_name='SessionID', blank=True)),
                ('email', models.EmailField(max_length=75, null=True, verbose_name='E-Mail', blank=True)),
                ('FIO', models.CharField(max_length=64, null=True, verbose_name='\u0424\u0418\u041e \u043f\u043e\u043a\u0443\u043f\u0430\u0442\u0435\u043b\u044f', blank=True)),
                ('phone', models.CharField(max_length=32, null=True, verbose_name='\u041d\u043e\u043c\u0435\u0440 \u043c\u043e\u0431\u0438\u043b\u044c\u043d\u043e\u0433\u043e \u0442\u0435\u043b\u0435\u0444\u043e\u043d\u0430', blank=True)),
                ('region', models.CharField(max_length=64, null=True, verbose_name='\u041e\u0431\u043b\u0430\u0441\u0442\u044c', blank=True)),
                ('settlement', models.CharField(max_length=64, null=True, verbose_name='\u041d\u0430\u0438\u043c\u0435\u043d\u043e\u0432\u0430\u043d\u0438\u0435 \u043d\u0430\u0441\u0435\u043b\u0451\u043d\u043d\u043e\u0433\u043e \u043f\u0443\u043d\u043a\u0442\u0430', blank=True)),
                ('warehouse_number', models.CharField(max_length=32, null=True, verbose_name='\u041d\u043e\u043c\u0435\u0440 \u0441\u043a\u043b\u0430\u0434\u0430 "\u041d\u043e\u0432\u043e\u0439 \u043f\u043e\u0447\u0442\u044b"', blank=True)),
                ('address', models.TextField(null=True, verbose_name='\u041f\u043e\u043b\u043d\u044b\u0439 \u0430\u0434\u0440\u0435\u0441\u0441', blank=True)),
                ('postcode', models.CharField(max_length=12, null=True, verbose_name='\u041f\u043e\u0447\u0442\u043e\u0432\u044b\u0439 \u0418\u043d\u0434\u0435\u043a\u0441 \u043f\u043e\u043b\u0443\u0447\u0430\u0442\u0435\u043b\u044f', blank=True)),
                ('comment', models.TextField(null=True, verbose_name='\u041a\u043e\u043c\u043c\u0435\u043d\u0442\u0430\u0440\u0438\u0439 \u043a \u0437\u0430\u043a\u0430\u0437\u0443', blank=True)),
                ('checkbox1', models.BooleanField(default=True, verbose_name='\u0416\u0434\u0443 \u0440\u0435\u043a\u0432\u0438\u0437\u0438\u0442\u044b')),
                ('checkbox2', models.BooleanField(default=False, verbose_name='\u0416\u0434\u0443 \u0437\u0432\u043e\u043d\u043a\u0430')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('country', models.ForeignKey(verbose_name='\u0421\u0442\u0440\u0430\u043d\u0430', to='product.Country')),
                ('delivery_company', models.ForeignKey(verbose_name='\u041a\u043e\u043c\u043f\u0430\u043d\u0438\u044f \u0434\u043e\u0441\u0442\u0430\u0432\u0449\u0438\u043a', blank=True, to='cart.DeliveryCompany', null=True)),
                ('user', models.ForeignKey(verbose_name='\u041f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044c', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ['-created_at'],
                'db_table': 'Order',
                'verbose_name': '\u0417\u0430\u043a\u0430\u0437',
                'verbose_name_plural': '\u0417\u0430\u043a\u0430\u0437\u044b',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.PositiveIntegerField(db_index=True)),
                ('quantity', models.PositiveSmallIntegerField(verbose_name='\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e \u043f\u0440\u043e\u0434\u0443\u043a\u0442\u043e\u0432')),
                ('price', models.DecimalField(default=0, verbose_name='\u0426\u0435\u043d\u0430 \u0432 \u0437\u0430\u0432\u0438\u0441\u0438\u043c\u043e\u0441\u0442\u0438 \u043e\u0442 \u043a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u0430', max_digits=8, decimal_places=2)),
                ('percentage_of_prepaid', models.PositiveSmallIntegerField(default=100, help_text='\u041f\u0440\u043e\u0446\u0435\u043d\u0442 \u043f\u0440\u0435\u0434\u043e\u043f\u043b\u0430\u0442\u044b \u0437\u0430 \u0434\u0430\u043d\u043d\u044b\u0439 \u0442\u043e\u0432\u0430\u0440.', verbose_name='\u041f\u0440\u043e\u0446\u0435\u043d\u0442 \u043f\u0440\u0435\u0434\u043e\u043f\u043b\u0430\u0442\u044b.')),
                ('available_to_order', models.NullBooleanField(default=None, help_text='\u041f\u043e\u043b\u0435 \u043f\u043e\u043a\u0430\u0437\u044b\u0432\u0430\u0435\u0442, \u0447\u0442\u043e \u044d\u0442\u043e\u0442 \u0442\u043e\u0432\u0430\u0440 \u0434\u043e\u0441\u0442\u0443\u043f\u0435\u043d \u0434\u043b\u044f \u0437\u0430\u043a\u0437\u0430. \u0415\u0441\u043b\u0438 \u0442\u043e\u0432\u0430\u0440 \u043d\u0435 \u0434\u043e\u0441\u0443\u0442\u043f\u0435\u043d \u0442\u043e \u043f\u043e\u043b\u0435 \u0431\u0443\u0434\u0435\u0442 False. \u0415\u0441\u043b\u0438 \u0442\u043e\u0432\u0430\u0440 \u0432 \u043d\u0430\u043b\u0438\u0447\u0438\u0438 \u043f\u043e \u043f\u043e\u043b\u043d\u043e\u0439 \u0441\u0442\u043e\u0438\u043c\u043e\u0441\u0442\u0438, \u0442\u043e \u043f\u043e\u043b\u0435 \u0431\u0443\u0434\u0435\u0442 Null', verbose_name='\u0414\u043e\u0441\u0442\u0443\u043f\u0435\u043d \u0434\u043b\u044f \u0437\u0430\u043a\u0430\u0437\u0430')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('content_type', models.ForeignKey(related_name='cart_or_order', verbose_name='\u041a\u043e\u0440\u0437\u0438\u043d\u0430', to='contenttypes.ContentType')),
                ('product', models.ForeignKey(verbose_name='\u041f\u0440\u043e\u0434\u0443\u043a\u0442', to='product.Product')),
            ],
            options={
                'ordering': ['-created_at'],
                'db_table': 'Product_in_Cart',
                'verbose_name': '\u041f\u0440\u043e\u0434\u0443\u043a\u0442 \u0432 \u043a\u043e\u0440\u0437\u0438\u043d\u0435',
                'verbose_name_plural': '\u041f\u0440\u043e\u0434\u0443\u043a\u0442\u044b \u0432 \u043a\u043e\u0440\u0437\u0438\u043d\u0435',
            },
            bases=(models.Model,),
        ),
    ]
