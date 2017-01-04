# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import apps.cart.models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0003_order_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='number',
            field=models.PositiveIntegerField(default=apps.cart.models.get_order_number, verbose_name='\u041d\u043e\u043c\u0435\u0440 \u0437\u0430\u043a\u0430\u0437\u0430'),
        ),
    ]
