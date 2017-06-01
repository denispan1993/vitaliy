# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0076_auto_20160823_1522'),
    ]

    operations = [
        migrations.AlterField(
            model_name='traceofvisits',
            name='email',
            field=models.ForeignKey(verbose_name='\u0423\u043a\u0430\u0437\u0430\u0442\u0435\u043b\u044c \u043d\u0430 E-Mail \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044f', blank=True, to='delivery.EmailForDelivery', null=True),
        ),
    ]
