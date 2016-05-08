# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coupon', '0006_auto_20160505_2146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='key',
            field=models.CharField(default=b'gb2w9g', unique=True, max_length=8, verbose_name='\u041a\u043b\u044e\u0447 \u043a\u0443\u043f\u043e\u043d\u0430'),
        ),
        migrations.AlterField(
            model_name='coupon',
            name='name',
            field=models.CharField(default=b'2016-05-07T21:45:36.232770', max_length=128, null=True, verbose_name='\u0418\u043c\u044f \u043a\u0443\u043f\u043e\u043d\u0430', blank=True),
        ),
        migrations.AlterField(
            model_name='coupongroup',
            name='name',
            field=models.CharField(default=b'2016-05-07T21:45:36.230001', max_length=128, null=True, verbose_name='\u0418\u043c\u044f \u0433\u0440\u0443\u043f\u043f\u044b \u043a\u0443\u043f\u043e\u043d\u043e\u0432', blank=True),
        ),
    ]
