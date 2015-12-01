# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0002_auto_20151113_1056'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'2015-12-01T15:24:18.923638', max_length=128, null=True, verbose_name='\u0418\u043c\u044f \u043a\u0443\u043f\u043e\u043d\u0430', blank=True)),
                ('key', models.CharField(default=b'5hhs2q', unique=True, max_length=8, verbose_name='\u041a\u043b\u044e\u0447 \u043a\u0443\u043f\u043e\u043d\u0430')),
                ('number_of_possible_uses', models.PositiveSmallIntegerField(default=1, verbose_name='\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e \u0432\u043e\u0437\u043c\u043e\u0436\u043d\u044b\u0445 \u0438\u0441\u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u043d\u0438\u0439')),
                ('number_of_uses', models.PositiveSmallIntegerField(default=0, verbose_name='\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e \u0438\u0441\u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u043d\u0438\u0439')),
                ('percentage_discount', models.PositiveSmallIntegerField(default=10, verbose_name='\u041f\u0440\u043e\u0446\u0435\u043d\u0442 \u0441\u043a\u0438\u0434\u043a\u0438')),
                ('start_of_the_coupon', models.DateTimeField(default=datetime.date(2015, 12, 1), verbose_name='\u0412\u0440\u044f\u043c\u044f \u043d\u0430\u0447\u0430\u043b\u0430 \u0434\u0435\u0439\u0441\u0442\u0432\u0438\u044f \u043a\u0443\u043f\u043e\u043d\u0430')),
                ('end_of_the_coupon', models.DateTimeField(default=datetime.date(2016, 3, 1), verbose_name='\u0412\u0440\u044f\u043c\u044f \u043e\u043a\u043e\u043d\u0447\u0430\u043d\u0438\u044f \u0434\u0435\u0439\u0441\u0442\u0432\u0438\u044f \u043a\u0443\u043f\u043e\u043d\u0430')),
                ('created_at', models.DateTimeField(default=datetime.datetime(2015, 12, 1, 15, 24, 18, 929337), verbose_name='\u0414\u0430\u0442\u0430 \u0441\u043e\u0437\u0434\u0430\u043d\u0438\u044f')),
                ('updated_at', models.DateTimeField(default=datetime.datetime(2015, 12, 1, 15, 24, 18, 929388), verbose_name='\u0414\u0430\u0442\u0430 \u043e\u0431\u043d\u043e\u0432\u043b\u0435\u043d\u0438\u044f')),
                ('child_cart', models.ManyToManyField(related_name='Cart_child', verbose_name='\u041a\u043e\u0440\u0437\u0438\u043d\u044b \u043a\u043e\u0442\u043e\u0440\u044b\u0435 \u0438\u0441\u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u043b\u0438 \u044d\u0442\u043e\u0442 \u043a\u0443\u043f\u043e\u043d', to='cart.Cart', blank=True)),
                ('child_order', models.ManyToManyField(related_name='Order_child', verbose_name='\u0417\u0430\u043a\u0430\u0437\u044b \u043a\u043e\u0442\u043e\u0440\u044b\u0435 \u0438\u0441\u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u043b\u0438 \u044d\u0442\u043e\u0442 \u043a\u0443\u043f\u043e\u043d', to='cart.Order', blank=True)),
            ],
            options={
                'ordering': ['-created_at'],
                'db_table': 'Coupon',
                'verbose_name': '\u041a\u0443\u043f\u043e\u043d',
                'verbose_name_plural': '\u041a\u0443\u043f\u043e\u043d\u044b',
            },
        ),
        migrations.CreateModel(
            name='CouponGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'2015-12-01T15:24:18.922262', max_length=128, null=True, verbose_name='\u0418\u043c\u044f \u0433\u0440\u0443\u043f\u043f\u044b \u043a\u0443\u043f\u043e\u043d\u043e\u0432', blank=True)),
                ('how_much_coupons', models.PositiveSmallIntegerField(default=10, null=True, verbose_name='\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e \u0441\u0433\u0435\u043d\u0435\u0440\u0438\u0440\u043e\u0432\u0430\u043d\u043d\u044b\u0445 \u043a\u0443\u043f\u043e\u043d\u043e\u0432', blank=True)),
                ('number_of_possible_uses', models.PositiveSmallIntegerField(default=1, null=True, verbose_name='\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e \u0432\u043e\u0437\u043c\u043e\u0436\u043d\u044b\u0445 \u0438\u0441\u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u043d\u0438\u0439', blank=True)),
                ('percentage_discount', models.PositiveSmallIntegerField(default=10, null=True, verbose_name='\u041f\u0440\u043e\u0446\u0435\u043d\u0442 \u0441\u043a\u0438\u0434\u043a\u0438', blank=True)),
                ('start_of_the_coupon', models.DateTimeField(default=datetime.date(2015, 12, 1), null=True, verbose_name='\u0412\u0440\u044f\u043c\u044f \u043d\u0430\u0447\u0430\u043b\u0430 \u0434\u0435\u0439\u0441\u0442\u0432\u0438\u044f \u043a\u0443\u043f\u043e\u043d\u043e\u0432', blank=True)),
                ('end_of_the_coupon', models.DateTimeField(default=datetime.date(2016, 3, 1), null=True, verbose_name='\u0412\u0440\u044f\u043c\u044f \u043e\u043a\u043e\u043d\u0447\u0430\u043d\u0438\u044f \u0434\u0435\u0439\u0441\u0442\u0432\u0438\u044f \u043a\u0443\u043f\u043e\u043d\u043e\u0432', blank=True)),
                ('created_at', models.DateTimeField(default=datetime.datetime(2015, 12, 1, 15, 24, 18, 922754), null=True, verbose_name='\u0414\u0430\u0442\u0430 \u0441\u043e\u0437\u0434\u0430\u043d\u0438\u044f', blank=True)),
                ('updated_at', models.DateTimeField(default=datetime.datetime(2015, 12, 1, 15, 24, 18, 922805), null=True, verbose_name='\u0414\u0430\u0442\u0430 \u043e\u0431\u043d\u043e\u0432\u043b\u0435\u043d\u0438\u044f', blank=True)),
            ],
            options={
                'ordering': ['-created_at'],
                'db_table': 'CouponGroup',
                'verbose_name': '\u0413\u0440\u0443\u043f\u043f\u0430 \u043a\u0443\u043f\u043e\u043d\u043e\u0432',
                'verbose_name_plural': '\u0413\u0440\u0443\u043f\u043f\u044b \u043a\u0443\u043f\u043e\u043d\u043e\u0432',
            },
        ),
        migrations.AddField(
            model_name='coupon',
            name='coupon_group',
            field=models.ForeignKey(blank=True, to='coupon.CouponGroup', help_text='\u0421\u0441\u044b\u043b\u043a\u0430 \u043d\u0430 \u0433\u0440\u0443\u043f\u0443 \u043a\u0443\u043f\u043e\u043d\u043e\u0432', null=True, verbose_name='\u0413\u0440\u0443\u043f\u043f\u0430 \u043a\u0443\u043f\u043e\u043d\u043e\u0432'),
        ),
        migrations.AddField(
            model_name='coupon',
            name='parent',
            field=models.ForeignKey(verbose_name='\u0417\u0430\u043a\u0430\u0437 \u043a\u043e\u0442\u043e\u0440\u044b\u0439 \u0441\u043e\u0437\u0434\u0430\u043b \u044d\u0442\u043e\u0442 \u043a\u0443\u043f\u043e\u043d', blank=True, to='cart.Order', null=True),
        ),
    ]
