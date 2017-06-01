# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0026_product_category'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['-title'], 'verbose_name': '\u041a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u044f', 'verbose_name_plural': '\u041a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u0438'},
        ),
        migrations.AddField(
            model_name='product',
            name='compare_with_1c',
            field=models.BooleanField(default=True, help_text='\u0415\u0441\u043b\u0438 \u0441\u0442\u043e\u0438\u0442 \u0433\u0430\u043b\u043e\u0447\u043a\u0430, \u0442\u043e \u044d\u0442\u043e\u0442 \u0442\u043e\u0432\u0430\u0440 \u0441\u0440\u0430\u0432\u043d\u0438\u0432\u0430\u0435\u0442\u0441\u044f \u043f\u043e \u043f\u0430\u0440\u0430\u043c\u0435\u0442\u0440\u0430\u043c \u0441 1\u0421', verbose_name='\u0421\u0440\u0430\u0432\u043d\u0438\u0432\u0430\u0442\u044c \u0441 1C'),
        ),
    ]
