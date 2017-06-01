# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0068_url_url_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Body',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('html', models.TextField(default='<html><head></head><body></body></html>', verbose_name='\u0422\u0435\u043b\u043e \u043f\u0438\u0441\u044c\u043c\u0430')),
                ('real_html', models.TextField(default='<html><head></head><body></body></html>', verbose_name='\u0422\u0435\u043b\u043e \u043f\u0438\u0441\u044c\u043c\u0430')),
                ('text', models.TextField(default='', verbose_name='\u0422\u0435\u043b\u043e \u043f\u0438\u0441\u044c\u043c\u0430')),
                ('chance', models.DecimalField(default=1, verbose_name='\u0412\u0435\u0440\u043e\u044f\u0442\u043d\u043e\u0441\u0442\u044c', max_digits=4, decimal_places=2)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='\u0414\u0430\u0442\u0430 \u0441\u043e\u0437\u0434\u0430\u043d\u0438\u044f', null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='\u0414\u0430\u0442\u0430 \u043e\u0431\u043d\u043e\u0432\u043b\u0435\u043d\u0438\u044f', null=True)),
            ],
            options={
                'ordering': ['-created_at'],
                'db_table': 'Delivery_body',
                'verbose_name': '\u0422\u0435\u043b\u043e \u043f\u0438\u0441\u044c\u043c\u0430',
                'verbose_name_plural': '\u0422\u0435\u043c\u0430 \u043f\u0438\u0441\u0435\u043c',
            },
        ),
        migrations.AddField(
            model_name='body',
            name='delivery',
            field=models.ForeignKey(to='delivery.Delivery'),
        ),
    ]
