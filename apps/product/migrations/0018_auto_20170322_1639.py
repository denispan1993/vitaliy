# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0017_category_bottom_description'),
    ]

    operations = [
        migrations.RenameField(
            model_name='currency',
            old_name='currency_code_number',
            new_name='currency_code_ISO_number',
        ),
        migrations.AddField(
            model_name='currency',
            name='currency_code_ISO_char',
            field=models.CharField(default=b'UAH', max_length=3, verbose_name='\u041a\u043e\u0434 \u0432\u0430\u043b\u044e\u0442\u044b \u0431\u0443\u043a\u0432\u0435\u043d\u043d\u044b\u0439'),
        ),
        migrations.AlterField(
            model_name='currency',
            name='currency_code_char',
            field=models.CharField(default='\u20b4', max_length=1, verbose_name='\u041a\u043e\u0434 \u0432\u0430\u043b\u044e\u0442\u044b \u043a\u043e\u0434'),
        ),
    ]
