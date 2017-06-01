# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0062_auto_20160714_1721'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('subject', models.CharField(default='\u0422\u0435\u043c\u0430', max_length=256, verbose_name='\u0422\u0435\u043c\u0430 \u043f\u0438\u0441\u044c\u043c\u0430')),
                ('chance', models.DecimalField(default=1, verbose_name='\u0412\u0435\u0440\u043e\u044f\u0442\u043d\u043e\u0441\u0442\u044c', max_digits=4, decimal_places=2)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='\u0414\u0430\u0442\u0430 \u0441\u043e\u0437\u0434\u0430\u043d\u0438\u044f', null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='\u0414\u0430\u0442\u0430 \u043e\u0431\u043d\u043e\u0432\u043b\u0435\u043d\u0438\u044f', null=True)),
            ],
            options={
                'ordering': ['-created_at'],
                'db_table': 'Subject',
                'verbose_name': '\u0422\u0435\u043c\u0430',
                'verbose_name_plural': '\u0422\u0435\u043c\u044b',
            },
        ),
        migrations.AlterModelOptions(
            name='emailmiddledelivery',
            options={'ordering': ['-created_at'],
                     'verbose_name': '\u041f\u0440\u043e\u043c\u0435\u0436\u0443\u0442\u043e\u0447\u043d\u0430\u044f \u043c\u043e\u0434\u0435\u043b\u044c \u0420\u0430\u0441\u0441\u044b\u043b\u043a\u0438', 'verbose_name_plural': '\u041f\u0440\u043e\u043c\u0435\u0436\u0443\u0442\u043e\u0447\u043d\u044b\u0435 \u043c\u043e\u0434\u0435\u043b\u0438 \u0420\u0430\u0441\u0441\u044b\u043b\u043e\u043a'},
        ),
        migrations.AddField(
            model_name='subject',
            name='delivery',
            field=models.ForeignKey(to='delivery.Delivery'),
        ),
    ]
