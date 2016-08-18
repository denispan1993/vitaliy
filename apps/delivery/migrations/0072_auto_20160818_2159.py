# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import apps.utils.captcha.views


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('delivery', '0071_auto_20160804_1710'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.PositiveIntegerField(db_index=True, null=True, blank=True)),
                ('direct_send', models.BooleanField(default=True, verbose_name='\u0428\u043b\u0435\u043c \u043d\u0430\u043f\u0440\u044f\u043c\u0443\u044e')),
                ('direct_email', models.EmailField(max_length=254, null=True, verbose_name='E-Mail \u043f\u0440\u044f\u043c\u043e\u0439 \u043e\u0442\u0441\u044b\u043b\u043a\u0438', blank=True)),
                ('subject_str', models.CharField(max_length=256, verbose_name='\u0421\u0442\u0440\u043e\u043a\u0430 subject')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='\u0414\u0430\u0442\u0430 \u0441\u043e\u0437\u0434\u0430\u043d\u0438\u044f', null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='\u0414\u0430\u0442\u0430 \u043e\u0431\u043d\u043e\u0432\u043b\u0435\u043d\u0438\u044f', null=True)),
                ('content_type', models.ForeignKey(verbose_name='\u0423\u043a\u0430\u0437\u0430\u0442\u0435\u043b\u044c \u043d\u0430 E-Mail', blank=True, to='contenttypes.ContentType', null=True)),
            ],
            options={
                'ordering': ['-created_at'],
                'db_table': 'Delivery_Message',
                'verbose_name': '\u0420\u0430\u0441\u0441\u044b\u043b\u043a\u0430 \u043e\u0442\u043e\u0441\u043b\u0430\u043d\u0430 \u043d\u0430 (Email \u0430\u0434\u0440\u0435\u0441)',
                'verbose_name_plural': '\u0420\u0430\u0441\u0441\u044b\u043b\u043a\u0438 \u043e\u0442\u043e\u0441\u043b\u0430\u043d\u044b \u043d\u0430 (Email \u0430\u0434\u0440\u0435\u0441\u0430)',
            },
        ),
        migrations.CreateModel(
            name='MessageUrl',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(default=apps.utils.captcha.views.key_generator, max_length=64, verbose_name='ID E-Mail \u0430\u0434\u0440\u0435\u0441\u0430 \u0440\u0430\u0441\u0441\u044b\u043b\u043a\u0438 \u0438 Url')),
                ('object_id', models.PositiveIntegerField(db_index=True, null=True, blank=True)),
                ('ready_url_str', models.CharField(max_length=256, verbose_name='\u0421\u0442\u0440\u043e\u043a\u0430 A tag')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='\u0414\u0430\u0442\u0430 \u0441\u043e\u0437\u0434\u0430\u043d\u0438\u044f', null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='\u0414\u0430\u0442\u0430 \u043e\u0431\u043d\u043e\u0432\u043b\u0435\u043d\u0438\u044f', null=True)),
                ('content_type', models.ForeignKey(verbose_name='\u0423\u043a\u0430\u0437\u0430\u0442\u0435\u043b\u044c \u043d\u0430 E-Mail', blank=True, to='contenttypes.ContentType', null=True)),
            ],
            options={
                'ordering': ['-created_at'],
                'db_table': 'Delivery_MessageUrl',
                'verbose_name': 'Message Url',
                'verbose_name_plural': 'Messages Urls',
            },
        ),
        migrations.CreateModel(
            name='SendEmailDelivery',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.PositiveIntegerField(db_index=True, null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='\u0414\u0430\u0442\u0430 \u0441\u043e\u0437\u0434\u0430\u043d\u0438\u044f', null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='\u0414\u0430\u0442\u0430 \u043e\u0431\u043d\u043e\u0432\u043b\u0435\u043d\u0438\u044f', null=True)),
                ('content_type', models.ForeignKey(verbose_name='\u0423\u043a\u0430\u0437\u0430\u0442\u0435\u043b\u044c \u043d\u0430 E-Mail', blank=True, to='contenttypes.ContentType', null=True)),
            ],
            options={
                'ordering': ['-created_at'],
                'db_table': 'Delivery_SendEmailDelivery',
                'verbose_name': '\u0420\u0430\u0441\u0441\u044b\u043b\u043a\u0430 \u043e\u0442\u043e\u0441\u043b\u0430\u043d\u0430 \u043d\u0430 (Email \u0430\u0434\u0440\u0435\u0441)',
                'verbose_name_plural': '\u0420\u0430\u0441\u0441\u044b\u043b\u043a\u0438 \u043e\u0442\u043e\u0441\u043b\u0430\u043d\u044b \u043d\u0430 (Email \u0430\u0434\u0440\u0435\u0441\u0430)',
            },
        ),
        migrations.RemoveField(
            model_name='url',
            name='str',
        ),
        migrations.AddField(
            model_name='url',
            name='anchor',
            field=models.CharField(default=b'http://keksik.com.ua/', max_length=256, verbose_name='\u042f\u043a\u043e\u0440\u044c --> "\u0410\u043d\u043a\u043e\u0440"'),
        ),
        migrations.AlterModelTable(
            name='delivery',
            table='Delivery_Delivery',
        ),
        migrations.AlterModelTable(
            name='emailfordelivery',
            table='Delivery_EmailForDelivery',
        ),
        migrations.AlterModelTable(
            name='emailmiddledelivery',
            table='Delivery_EmailMiddleDelivery',
        ),
        migrations.AlterModelTable(
            name='mailaccount',
            table='Delivery_MailAccount',
        ),
        migrations.AlterModelTable(
            name='mailserver',
            table='Delivery_MailServer',
        ),
        migrations.AlterModelTable(
            name='rawemail',
            table='Delivery_RawEmail',
        ),
        migrations.AlterModelTable(
            name='spamemail',
            table='Delivery_SpamEmail',
        ),
        migrations.AlterModelTable(
            name='subject',
            table='Delivery_Subject',
        ),
        migrations.AlterModelTable(
            name='traceofvisits',
            table='Delivery_TraceOfVisits',
        ),
        migrations.AlterModelTable(
            name='url',
            table='Delivery_Url',
        ),
        migrations.AddField(
            model_name='sendemaildelivery',
            name='delivery',
            field=models.ForeignKey(verbose_name='\u0423\u043a\u0430\u0437\u0430\u0442\u0435\u043b\u044c \u043d\u0430 \u0440\u0430\u0441\u0441\u044b\u043b\u043a\u0443', to='delivery.Delivery'),
        ),
        migrations.AddField(
            model_name='messageurl',
            name='delivery',
            field=models.ForeignKey(verbose_name='\u0423\u043a\u0430\u0437\u0430\u0442\u0435\u043b\u044c \u043d\u0430 \u0440\u0430\u0441\u0441\u044b\u043b\u043a\u0443', to='delivery.Delivery'),
        ),
        migrations.AddField(
            model_name='messageurl',
            name='message',
            field=models.ForeignKey(verbose_name='\u0423\u043a\u0430\u0437\u0430\u0442\u0435\u043b\u044c \u043d\u0430 \u0441\u043e\u043e\u0431\u0449\u0435\u043d\u0438\u0435', to='delivery.Message'),
        ),
        migrations.AddField(
            model_name='messageurl',
            name='url',
            field=models.ForeignKey(verbose_name='\u0423\u043a\u0430\u0437\u0430\u0442\u0435\u043b\u044c \u043d\u0430 Url', to='delivery.Url'),
        ),
        migrations.AddField(
            model_name='message',
            name='delivery',
            field=models.ForeignKey(verbose_name='\u0423\u043a\u0430\u0437\u0430\u0442\u0435\u043b\u044c \u043d\u0430 \u0440\u0430\u0441\u0441\u044b\u043b\u043a\u0443', to='delivery.Delivery'),
        ),
        migrations.AddField(
            model_name='message',
            name='sender_account',
            field=models.ForeignKey(verbose_name='Account \u043d\u0435 \u043f\u0440\u044f\u043c\u043e\u0439 \u043e\u0442\u0441\u044b\u043b\u043a\u0438', blank=True, to='delivery.MailAccount', null=True),
        ),
        migrations.AddField(
            model_name='message',
            name='subject',
            field=models.ForeignKey(verbose_name='\u0423\u043a\u0430\u0437\u0430\u0442\u0435\u043b\u044c \u043d\u0430 subject', to='delivery.Subject'),
        ),
    ]
