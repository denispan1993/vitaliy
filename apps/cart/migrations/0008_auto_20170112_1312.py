# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0007_auto_20170111_1714'),
    ]

    operations = [
        migrations.CreateModel(
            name='Template',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64, unique=True, null=True, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435', blank=True)),
                ('is_system', models.BooleanField(default=False, verbose_name='\u0421\u0438\u0441\u0442\u0435\u043c\u043d\u044b\u0439')),
                ('template', models.TextField(null=True, verbose_name='\u0428\u0430\u0431\u043b\u043e\u043d', blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='\u0414\u0430\u0442\u0430 \u0441\u043e\u0437\u0434\u0430\u043d\u0438\u044f', null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='\u0414\u0430\u0442\u0430 \u043e\u0431\u043d\u043e\u0432\u043b\u0435\u043d\u0438\u044f', null=True)),
            ],
            options={
                'ordering': ['-created_at'],
                'db_table': 'Cart_Template',
                'verbose_name': 'Template \u043f\u0438\u0441\u044c\u043c\u0430',
                'verbose_name_plural': 'Templates \u043f\u0438\u0441\u0435\u043c',
            },
        ),
        migrations.AlterField(
            model_name='order',
            name='sent_out_sum',
            field=models.DecimalField(null=True, verbose_name='\u041e\u0442\u043e\u0441\u043b\u0430\u043d\u043d\u0430\u044f \u0441\u0443\u043c\u043c\u0430 \u0437\u0430\u043a\u0430\u0437\u0430', max_digits=8, decimal_places=2, blank=True),
        ),
    ]
