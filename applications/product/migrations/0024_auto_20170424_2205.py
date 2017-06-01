# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0023_auto_20170424_2140'),
    ]

    operations = [
        migrations.RunSQL("INSERT INTO ProductToCategory (product_id, category_id, created_at, updated_at)"
                          "SELECT product_id, category_id, now(), now() FROM Product_category"
# SQLite
#        migrations.RunSQL("INSERT INTO ProductToCategory (product_id, category_id, created_at, updated_at)"
#                          "SELECT product_id, category_id, datetime('now','localtime'), datetime('now','localtime') FROM Product_category"
        ),
    ]
