# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
import django.utils.timezone
import apps.coupon.models


class Migration(migrations.Migration):

    dependencies = [
        ('coupon', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='\u0414\u0430\u0442\u0430 \u0441\u043e\u0437\u0434\u0430\u043d\u0438\u044f'),
        ),
        migrations.AlterField(
            model_name='coupon',
            name='end_of_the_coupon',
            field=models.DateTimeField(default=apps.coupon.models.add_three_month, verbose_name='\u0412\u0440\u044f\u043c\u044f \u043e\u043a\u043e\u043d\u0447\u0430\u043d\u0438\u044f \u0434\u0435\u0439\u0441\u0442\u0432\u0438\u044f \u043a\u0443\u043f\u043e\u043d\u0430'),
        ),
        migrations.AlterField(
            model_name='coupon',
            name='key',
            field=models.CharField(default=b'w93x0v', unique=True, max_length=8, verbose_name='\u041a\u043b\u044e\u0447 \u043a\u0443\u043f\u043e\u043d\u0430'),
        ),
        migrations.AlterField(
            model_name='coupon',
            name='name',
            field=models.CharField(default=b'2015-12-01T15:37:24.961364', max_length=128, null=True, verbose_name='\u0418\u043c\u044f \u043a\u0443\u043f\u043e\u043d\u0430', blank=True),
        ),
        migrations.AlterField(
            model_name='coupon',
            name='start_of_the_coupon',
            field=models.DateTimeField(default=datetime.date.today, verbose_name='\u0412\u0440\u044f\u043c\u044f \u043d\u0430\u0447\u0430\u043b\u0430 \u0434\u0435\u0439\u0441\u0442\u0432\u0438\u044f \u043a\u0443\u043f\u043e\u043d\u0430'),
        ),
        migrations.AlterField(
            model_name='coupon',
            name='updated_at',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='\u0414\u0430\u0442\u0430 \u043e\u0431\u043d\u043e\u0432\u043b\u0435\u043d\u0438\u044f'),
        ),
        migrations.AlterField(
            model_name='coupongroup',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, null=True, verbose_name='\u0414\u0430\u0442\u0430 \u0441\u043e\u0437\u0434\u0430\u043d\u0438\u044f', blank=True),
        ),
        migrations.AlterField(
            model_name='coupongroup',
            name='end_of_the_coupon',
            field=models.DateTimeField(default=apps.coupon.models.add_three_month, null=True, verbose_name='\u0412\u0440\u044f\u043c\u044f \u043e\u043a\u043e\u043d\u0447\u0430\u043d\u0438\u044f \u0434\u0435\u0439\u0441\u0442\u0432\u0438\u044f \u043a\u0443\u043f\u043e\u043d\u043e\u0432', blank=True),
        ),
        migrations.AlterField(
            model_name='coupongroup',
            name='name',
            field=models.CharField(default=b'2015-12-01T15:37:24.960218', max_length=128, null=True, verbose_name='\u0418\u043c\u044f \u0433\u0440\u0443\u043f\u043f\u044b \u043a\u0443\u043f\u043e\u043d\u043e\u0432', blank=True),
        ),
        migrations.AlterField(
            model_name='coupongroup',
            name='start_of_the_coupon',
            field=models.DateTimeField(default=datetime.date.today, null=True, verbose_name='\u0412\u0440\u044f\u043c\u044f \u043d\u0430\u0447\u0430\u043b\u0430 \u0434\u0435\u0439\u0441\u0442\u0432\u0438\u044f \u043a\u0443\u043f\u043e\u043d\u043e\u0432', blank=True),
        ),
        migrations.AlterField(
            model_name='coupongroup',
            name='updated_at',
            field=models.DateTimeField(default=django.utils.timezone.now, null=True, verbose_name='\u0414\u0430\u0442\u0430 \u043e\u0431\u043d\u043e\u0432\u043b\u0435\u043d\u0438\u044f', blank=True),
        ),
    ]
