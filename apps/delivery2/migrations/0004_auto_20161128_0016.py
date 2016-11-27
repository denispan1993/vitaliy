# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery2', '0003_auto_20161126_1937'),
    ]

    operations = [
        migrations.CreateModel(
            name='MessageRedirectUrl',
            fields=[
                ('id', models.BigIntegerField(serialize=False, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='\u0414\u0430\u0442\u0430 \u0441\u043e\u0437\u0434\u0430\u043d\u0438\u044f', null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='\u0414\u0430\u0442\u0430 \u043e\u0431\u043d\u043e\u0432\u043b\u0435\u043d\u0438\u044f', null=True)),
                ('delivery', models.ForeignKey(verbose_name='\u0420\u0430\u0441\u0441\u044b\u043b\u043a\u0430', to='delivery2.Delivery')),
                ('href', models.ForeignKey(verbose_name='Url', blank=True, to='delivery2.EmailUrlTemplate', null=True)),
            ],
            options={
                'ordering': ['-created_at'],
                'db_table': 'Delivery2_MessageRedirectUrl',
                'verbose_name': 'Url',
                'verbose_name_plural': 'Urls',
            },
        ),
        migrations.RemoveField(
            model_name='redirecturl',
            name='delivery',
        ),
        migrations.AlterField(
            model_name='emailsubject',
            name='delivery',
            field=models.ForeignKey(related_name='subjects', to='delivery2.Delivery'),
        ),
        migrations.AlterField(
            model_name='emailtemplate',
            name='delivery',
            field=models.ForeignKey(related_name='templates', to='delivery2.Delivery'),
        ),
        migrations.DeleteModel(
            name='RedirectUrl',
        ),
    ]
