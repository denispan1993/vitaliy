# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0020_product_quantity_in_stock'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductToCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('category', models.ForeignKey(to='product.Category')),
                ('product', models.ForeignKey(to='product.Product')),
            ],
            options={
                'db_table': 'ProductToCategory',
            },
        ),
    ]
