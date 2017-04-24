# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0021_producttocategory'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='producttocategory',
            unique_together=set([('product', 'category')]),
        ),
    ]
