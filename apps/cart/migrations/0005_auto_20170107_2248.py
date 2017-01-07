# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0004_auto_20170102_2258'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='custom_order_sum',
            field=models.PositiveIntegerField(null=True, verbose_name='\u0421\u0443\u043c\u043c\u0430 \u0437\u0430\u043a\u0430\u0437\u0430 \u0432 \u0440\u0443\u0447\u043d\u0443\u044e', blank=True),
        ),
        migrations.AddField(
            model_name='product',
            name='custom_price',
            field=models.BooleanField(default=False, verbose_name='\u0426\u0435\u043d\u0430 \u0443\u0441\u0442\u0430\u043d\u043e\u0432\u043b\u0435\u043d\u043d\u0430\u044f \u0432 \u0440\u0443\u0447\u043d\u0443\u044e'),
        ),
    ]
