# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authModel', '0003_auto_20151117_2224'),
    ]

    operations = [
        migrations.AddField(
            model_name='email',
            name='description',
            field=models.TextField(help_text='\u041f\u043e\u043b\u0435 \u0441 \u0442\u0435\u043a\u0441\u0442\u043e\u0432\u044b\u043c \u043e\u043f\u0438\u0441\u0430\u043d\u0438\u0435\u043c', null=True, verbose_name='\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435', blank=True),
        ),
    ]
