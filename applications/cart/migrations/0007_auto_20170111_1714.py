# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0006_auto_20170108_1745'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='custom_order_sum',
        ),
        migrations.AddField(
            model_name='order',
            name='custom_sum',
            field=models.BooleanField(default=False, verbose_name='\u0421\u0443\u043c\u043c\u0430 \u0437\u0430\u043a\u0430\u0437\u0430 \u0432\u0432\u0435\u0434\u0435\u043d\u0430 \u0430 \u0440\u0443\u0447\u043d\u0443\u044e'),
        ),
        migrations.AddField(
            model_name='order',
            name='sent_out_sum',
            field=models.PositiveIntegerField(null=True, verbose_name='\u041e\u0442\u043e\u0441\u043b\u0430\u043d\u043d\u0430\u044f \u0441\u0443\u043c\u043c\u0430 \u0437\u0430\u043a\u0430\u0437\u0430', blank=True),
        ),
    ]
