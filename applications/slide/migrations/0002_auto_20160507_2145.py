# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('slide', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='slide',
            name='name',
            field=models.CharField(default='\u0421\u043b\u0430\u0439\u0434 \u043e\u0442 2016-05-07 21:45:36.395377', max_length=128, null=True, verbose_name='\u041d\u0430\u0438\u043c\u0435\u043d\u043e\u0432\u0430\u043d\u0438\u0435 \u0441\u043b\u0430\u0439\u0434\u0430', blank=True),
        ),
    ]
