# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0016_product_id_1c'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='bottom_description',
            field=models.TextField(null=True, verbose_name='\u041d\u0438\u0436\u043d\u0435\u0435 \u043e\u043f\u0438\u0441\u0430\u043d\u0438\u0435 \u043a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u0438', blank=True),
        ),
    ]
