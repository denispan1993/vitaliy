# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0027_auto_20170530_1459'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemid',
            name='ItemID',
            field=models.CharField(db_index=True, max_length=32, null=True, verbose_name='ItemID', blank=True),
        ),
        migrations.AlterField(
            model_name='itemid',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='itemid',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='id_1c',
            field=models.CharField(max_length=36, blank=True, help_text='\u041a\u043e\u0434 1\u0421', null=True, verbose_name='1C \u0418\u0434', db_index=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(db_index=True, max_length=255, null=True, verbose_name='\u041d\u0430\u0438\u043c\u0435\u043d\u043e\u0432\u0430\u043d\u0438\u0435 \u043f\u0440\u043e\u0434\u0443\u043a\u0442\u0430', blank=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='serial_number',
            field=models.PositiveSmallIntegerField(default=1, null=True, verbose_name='\u041f\u043e\u0440\u044f\u0434\u043e\u043a \u0441\u043e\u0440\u0442\u0438\u0440\u043e\u0432\u043a\u0438', db_index=True, blank=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='title',
            field=models.CharField(max_length=255, verbose_name='\u0417\u0430\u0433\u043e\u043b\u043e\u0432\u043e\u043a \u043f\u0440\u043e\u0434\u0443\u043a\u0442\u0430', db_index=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='view',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='view',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='viewed',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='\u0414\u0430\u0442\u0430 \u0434\u043e\u0431\u0430\u0432\u043b\u0435\u043d\u0438\u044f', db_index=True),
        ),
        migrations.AlterField(
            model_name='viewed',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='\u0414\u0430\u0442\u0430 \u043f\u043e\u0441\u043b\u0435\u0434\u043d\u0435\u0433\u043e \u0438\u0437\u043c\u0435\u043d\u0435\u043d\u0438\u044f', db_index=True),
        ),
    ]
