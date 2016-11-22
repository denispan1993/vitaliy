# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import apps.delivery2.models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Delivery',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=apps.delivery2.models.datetime_in_iso_format, max_length=128, null=True, verbose_name='\u0418\u043c\u044f \u0440\u0430\u0441\u0441\u044b\u043b\u043a\u0438', blank=True)),
                ('can_send', models.BooleanField(default=False, verbose_name='\u0420\u0430\u0437\u0440\u0435\u0448\u0435\u043d\u043e \u043e\u0442\u043f\u0440\u0430\u0432\u043b\u044f\u0442\u044c \u0440\u0430\u0441\u0441\u044b\u043b\u043a\u0443')),
                ('is_active', models.BooleanField(default=False, verbose_name='\u0420\u0430\u0441\u0441\u044b\u043b\u043a\u0430 \u0438\u0434\u0435\u0442')),
                ('task_id', models.CharField(verbose_name='task id', max_length=255, null=True, editable=False, blank=True)),
                ('delivery_test', models.BooleanField(default=True, verbose_name='\u0422\u0435\u0441\u0442\u043e\u0432\u0430\u044f \u0440\u0430\u0441\u0441\u044b\u043b\u043a\u0430')),
                ('test_send', models.BooleanField(default=False, verbose_name='\u0422\u0435\u0441\u0442\u043e\u0432\u0430\u044f \u0440\u0430\u0441\u0441\u044b\u043b\u043a\u0430 \u043e\u0442\u043e\u0441\u043b\u0430\u043d\u0430')),
                ('general_send', models.BooleanField(default=False, verbose_name='\u0413\u043b\u0430\u0432\u043d\u0430\u044f \u0440\u0430\u0441\u0441\u044b\u043b\u043a\u0430 \u043e\u0442\u043e\u0441\u043b\u0430\u043d\u0430')),
                ('type', models.PositiveSmallIntegerField(default=1, verbose_name='\u0422\u0438\u043f \u0440\u0430\u0441\u0441\u044b\u043b\u043a\u0438', choices=[(1, '\u0421\u0438\u0441\u0442\u0435\u043c\u043d\u0430\u044f'), (2, '\u0410\u043a\u0446\u0438\u044f'), (4, '\u041d\u043e\u0432\u0438\u043d\u043a\u0438')])),
                ('started_at', models.DateTimeField(null=True, verbose_name='\u0414\u0430\u0442\u0430 \u0438 \u0432\u0440\u0435\u043c\u044f \u0440\u0430\u0441\u0441\u044b\u043b\u043a\u0438', blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='\u0414\u0430\u0442\u0430 \u0441\u043e\u0437\u0434\u0430\u043d\u0438\u044f', null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='\u0414\u0430\u0442\u0430 \u043e\u0431\u043d\u043e\u0432\u043b\u0435\u043d\u0438\u044f', null=True)),
            ],
            options={
                'ordering': ['-created_at'],
                'db_table': 'Delivery2_Delivery',
                'verbose_name': '\u0420\u0430\u0441\u0441\u044b\u043b\u043a\u0430',
                'verbose_name_plural': '\u0420\u0430\u0441\u0441\u044b\u043b\u043a\u0438',
            },
        ),
        migrations.CreateModel(
            name='EmailTemplate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('template', models.FileField(upload_to=apps.delivery2.models.upload_to, verbose_name='\u0428\u0430\u0431\u043b\u043e\u043d')),
                ('chance', models.DecimalField(default=1, verbose_name='\u0412\u0435\u0440\u043e\u044f\u0442\u043d\u043e\u0441\u0442\u044c', max_digits=4, decimal_places=2)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='\u0414\u0430\u0442\u0430 \u0441\u043e\u0437\u0434\u0430\u043d\u0438\u044f', null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='\u0414\u0430\u0442\u0430 \u043e\u0431\u043d\u043e\u0432\u043b\u0435\u043d\u0438\u044f', null=True)),
                ('delivery', models.ForeignKey(to='delivery2.Delivery')),
            ],
            options={
                'ordering': ['-created_at'],
                'db_table': 'Delivery2_Template',
                'verbose_name': '\u0422\u0435\u043b\u043e \u043f\u0438\u0441\u044c\u043c\u0430',
                'verbose_name_plural': '\u0422\u0435\u043c\u0430 \u043f\u0438\u0441\u0435\u043c',
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_send', models.BooleanField(default=False, verbose_name='\u0420\u0430\u0441\u0441\u044b\u043b\u043a\u0430 \u043e\u0442\u043e\u0441\u043b\u0430\u043d\u0430')),
                ('object_id', models.PositiveIntegerField(db_index=True, null=True, blank=True)),
                ('subject_str', models.CharField(max_length=256, null=True, verbose_name='\u0421\u0442\u0440\u043e\u043a\u0430 subject', blank=True)),
                ('template_body', models.TextField(null=True, verbose_name='Template body', blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='\u0414\u0430\u0442\u0430 \u0441\u043e\u0437\u0434\u0430\u043d\u0438\u044f', null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='\u0414\u0430\u0442\u0430 \u043e\u0431\u043d\u043e\u0432\u043b\u0435\u043d\u0438\u044f', null=True)),
                ('content_type', models.ForeignKey(related_name='delivery_Message', verbose_name='\u0423\u043a\u0430\u0437\u0430\u0442\u0435\u043b\u044c \u043d\u0430 E-Mail', blank=True, to='contenttypes.ContentType', null=True)),
                ('delivery', models.ForeignKey(verbose_name='\u0423\u043a\u0430\u0437\u0430\u0442\u0435\u043b\u044c \u043d\u0430 \u0440\u0430\u0441\u0441\u044b\u043b\u043a\u0443', to='delivery2.Delivery')),
            ],
            options={
                'ordering': ['-created_at'],
                'db_table': 'Delivery2_Message',
                'verbose_name': '\u0420\u0430\u0441\u0441\u044b\u043b\u043a\u0430 \u043e\u0442\u043e\u0441\u043b\u0430\u043d\u0430 \u043d\u0430 (Email \u0430\u0434\u0440\u0435\u0441)',
                'verbose_name_plural': '\u0420\u0430\u0441\u0441\u044b\u043b\u043a\u0438 \u043e\u0442\u043e\u0441\u043b\u0430\u043d\u044b \u043d\u0430 (Email \u0430\u0434\u0440\u0435\u0441\u0430)',
            },
        ),
        migrations.CreateModel(
            name='RedirectUrl',
            fields=[
                ('id', models.BigIntegerField(serialize=False, primary_key=True)),
                ('href', models.CharField(default=b'http://keksik.com.ua/', max_length=256, verbose_name='URL')),
                ('uuid', models.CharField(default=b'http://keksik.com.ua/', max_length=256, verbose_name='UUID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='\u0414\u0430\u0442\u0430 \u0441\u043e\u0437\u0434\u0430\u043d\u0438\u044f', null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='\u0414\u0430\u0442\u0430 \u043e\u0431\u043d\u043e\u0432\u043b\u0435\u043d\u0438\u044f', null=True)),
                ('delivery', models.ForeignKey(verbose_name='\u0420\u0430\u0441\u0441\u044b\u043b\u043a\u0430', to='delivery2.Delivery')),
            ],
            options={
                'ordering': ['-created_at'],
                'db_table': 'Delivery2_RedirectUrl',
                'verbose_name': 'Url',
                'verbose_name_plural': 'Urls',
            },
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('subject', models.CharField(default='\u0422\u0435\u043c\u0430', max_length=256, verbose_name='\u0422\u0435\u043c\u0430 \u043f\u0438\u0441\u044c\u043c\u0430')),
                ('chance', models.DecimalField(default=1, verbose_name='\u0412\u0435\u0440\u043e\u044f\u0442\u043d\u043e\u0441\u0442\u044c', max_digits=4, decimal_places=2)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='\u0414\u0430\u0442\u0430 \u0441\u043e\u0437\u0434\u0430\u043d\u0438\u044f', null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='\u0414\u0430\u0442\u0430 \u043e\u0431\u043d\u043e\u0432\u043b\u0435\u043d\u0438\u044f', null=True)),
                ('delivery', models.ForeignKey(to='delivery2.Delivery')),
            ],
            options={
                'ordering': ['-created_at'],
                'db_table': 'Delivery2_Subject',
                'verbose_name': '\u0422\u0435\u043c\u0430',
                'verbose_name_plural': '\u0422\u0435\u043c\u044b',
            },
        ),
        migrations.AddField(
            model_name='message',
            name='subject',
            field=models.ForeignKey(verbose_name='\u0423\u043a\u0430\u0437\u0430\u0442\u0435\u043b\u044c \u043d\u0430 subject', blank=True, to='delivery2.Subject', null=True),
        ),
        migrations.AddField(
            model_name='message',
            name='template',
            field=models.ForeignKey(verbose_name='Template', blank=True, to='delivery2.EmailTemplate', null=True),
        ),
        migrations.AddField(
            model_name='delivery',
            name='template',
            field=models.ForeignKey(related_name='delivery_EmailTemplate', verbose_name='Template', blank=True, to='delivery2.EmailTemplate', null=True),
        ),
    ]
