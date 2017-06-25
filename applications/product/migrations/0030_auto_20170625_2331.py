# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-25 20:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0029_auto_20170607_2151'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Unit_of_Measurement',
            new_name='UnitofMeasurement',
        ),
        migrations.AlterField(
            model_name='category',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='title',
            field=models.CharField(db_index=True, max_length=255, verbose_name='Заголовок категории'),
        ),
        migrations.AlterField(
            model_name='category',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='currency',
            name='currency_code_ISO_number',
            field=models.PositiveSmallIntegerField(db_index=True, default=0, verbose_name='Код валюты числовой'),
        ),
        migrations.AlterField(
            model_name='product',
            name='in_main_page',
            field=models.BooleanField(db_index=True, default=False, help_text='Если мы хотим чтобы продукт показывался на главной странице ставим данное поле в True.', verbose_name='На главной странице'),
        ),
    ]
