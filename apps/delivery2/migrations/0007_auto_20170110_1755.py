# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery2', '0006_auto_20170110_1642'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailtemplate',
            name='delivery',
            field=models.ForeignKey(related_name='templates', blank=True, to='delivery2.Delivery', null=True),
        ),
    ]
