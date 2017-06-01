# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('delivery2', '0002_auto_20161124_2123'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailUrlTemplate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('href', models.CharField(max_length=256, null=True, verbose_name='URL', blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='\u0414\u0430\u0442\u0430 \u0441\u043e\u0437\u0434\u0430\u043d\u0438\u044f', null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='\u0414\u0430\u0442\u0430 \u043e\u0431\u043d\u043e\u0432\u043b\u0435\u043d\u0438\u044f', null=True)),
            ],
            options={
                'ordering': ['-created_at'],
                'db_table': 'Delivery2_EmailUrlTemplate',
                'verbose_name': 'Url \u0432 \u0442\u0435\u043c\u043f\u043b\u044d\u0439\u0442\u0435',
                'verbose_name_plural': 'Urls \u0432 \u0442\u0435\u043c\u043f\u043b\u044d\u0439\u0442\u0435',
            },
        ),
        migrations.AlterModelOptions(
            name='emailtemplate',
            options={'ordering': ['-created_at'], 'verbose_name': 'Template \u043f\u0438\u0441\u044c\u043c\u0430', 'verbose_name_plural': 'Templates \u043f\u0438\u0441\u0435\u043c'},
        ),
        migrations.AlterField(
            model_name='emailsubject',
            name='subject',
            field=models.CharField(default=datetime.datetime.now, max_length=256, verbose_name='\u0422\u0435\u043c\u0430 \u043f\u0438\u0441\u044c\u043c\u0430'),
        ),
        migrations.AlterField(
            model_name='emailtemplate',
            name='name',
            field=models.CharField(null=True, default=datetime.datetime.now, max_length=64, blank=True, unique=True, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435'),
        ),
        migrations.AlterField(
            model_name='message',
            name='subject',
            field=models.ForeignKey(verbose_name='Subject', blank=True, to='delivery2.EmailSubject', null=True),
        ),
        migrations.AlterField(
            model_name='message',
            name='subject_str',
            field=models.CharField(max_length=256, null=True, verbose_name='Subject str', blank=True),
        ),
        migrations.AddField(
            model_name='emailurltemplate',
            name='template',
            field=models.ForeignKey(related_name='urls', verbose_name='\u0428\u0430\u0431\u043b\u043e\u043d', to='delivery2.EmailTemplate'),
        ),
    ]
