# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0025_remove_product_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ManyToManyField(related_name='products', verbose_name='\u041a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u0438', through='product.ProductToCategory', to='product.Category'),
        ),
    ]
