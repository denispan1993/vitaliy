# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import applications.delivery2.models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery2', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailImageTemplate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.CharField(max_length=256, verbose_name='\u041f\u0443\u0442\u044c')),
                ('image', models.ImageField(upload_to=applications.delivery2.models.upload_to, null=True, verbose_name='\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435', blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='\u0414\u0430\u0442\u0430 \u0441\u043e\u0437\u0434\u0430\u043d\u0438\u044f', null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='\u0414\u0430\u0442\u0430 \u043e\u0431\u043d\u043e\u0432\u043b\u0435\u043d\u0438\u044f', null=True)),
            ],
            options={
                'ordering': ['-created_at'],
                'db_table': 'Delivery2_EmailImageTemplate',
                'verbose_name': '\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0432 \u043f\u0438\u0441\u044c\u043c\u0435',
                'verbose_name_plural': '\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u044f \u0432 \u043f\u0438\u0441\u044c\u043c\u0435',
            },
        ),
        migrations.CreateModel(
            name='EmailSubject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('subject', models.CharField(default='\u0422\u0435\u043c\u0430', max_length=256, verbose_name='\u0422\u0435\u043c\u0430 \u043f\u0438\u0441\u044c\u043c\u0430')),
                ('chance', models.DecimalField(default=1, verbose_name='\u0412\u0435\u0440\u043e\u044f\u0442\u043d\u043e\u0441\u0442\u044c', max_digits=4, decimal_places=2)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='\u0414\u0430\u0442\u0430 \u0441\u043e\u0437\u0434\u0430\u043d\u0438\u044f', null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='\u0414\u0430\u0442\u0430 \u043e\u0431\u043d\u043e\u0432\u043b\u0435\u043d\u0438\u044f', null=True)),
            ],
            options={
                'ordering': ['-created_at'],
                'db_table': 'Delivery2_EmailSubject',
                'verbose_name': '\u0422\u0435\u043c\u0430',
                'verbose_name_plural': '\u0422\u0435\u043c\u044b',
            },
        ),
        migrations.RemoveField(
            model_name='subject',
            name='delivery',
        ),
        migrations.RemoveField(
            model_name='delivery',
            name='template',
        ),
        migrations.AddField(
            model_name='emailtemplate',
            name='name',
            field=models.CharField(null=True, default=b'<built-in method now of type object at 0x83c4c20>', max_length=64, blank=True, unique=True, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435'),
        ),
        migrations.AlterField(
            model_name='delivery',
            name='task_id',
            field=models.CharField(max_length=255, null=True, verbose_name='task id', blank=True),
        ),
        migrations.AlterField(
            model_name='emailtemplate',
            name='template',
            field=models.FileField(upload_to=applications.delivery2.models.upload_to, null=True, verbose_name='\u0428\u0430\u0431\u043b\u043e\u043d', blank=True),
        ),
        migrations.AlterField(
            model_name='message',
            name='subject',
            field=models.ForeignKey(verbose_name='\u0423\u043a\u0430\u0437\u0430\u0442\u0435\u043b\u044c \u043d\u0430 subject', blank=True, to='delivery2.EmailSubject', null=True),
        ),
        migrations.AlterModelTable(
            name='emailtemplate',
            table='Delivery2_EmailTemplate',
        ),
        migrations.DeleteModel(
            name='Subject',
        ),
        migrations.AddField(
            model_name='emailsubject',
            name='delivery',
            field=models.ForeignKey(to='delivery2.Delivery'),
        ),
        migrations.AddField(
            model_name='emailimagetemplate',
            name='template',
            field=models.ForeignKey(related_name='images', verbose_name='\u0428\u0430\u0431\u043b\u043e\u043d', to='delivery2.EmailTemplate'),
        ),
    ]
