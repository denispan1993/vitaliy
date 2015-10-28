# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0035_auto_20151028_1640'),
    ]

    operations = [
        migrations.CreateModel(
            name='MailAccount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.CharField(max_length=64, verbose_name='E-Mail')),
                ('login', models.CharField(max_length=64, verbose_name='UserName - login')),
                ('password', models.CharField(max_length=64, verbose_name='User password')),
                ('created_at', models.DateTimeField(default=datetime.datetime(2015, 10, 28, 16, 48, 36, 600036), auto_now_add=True, null=True, verbose_name='\u0414\u0430\u0442\u0430 \u0441\u043e\u0437\u0434\u0430\u043d\u0438\u044f')),
                ('updated_at', models.DateTimeField(default=datetime.datetime(2015, 10, 28, 16, 48, 36, 600067), auto_now=True, null=True, verbose_name='\u0414\u0430\u0442\u0430 \u043e\u0431\u043d\u043e\u0432\u043b\u0435\u043d\u0438\u044f')),
                ('server', models.ForeignKey(verbose_name='SMTP Server', to='delivery.MailServer')),
            ],
            options={
                'ordering': ['-created_at'],
                'db_table': 'MailAccount',
                'verbose_name': 'SMTP Account',
                'verbose_name_plural': 'SMTP Accounts',
            },
            bases=(models.Model,),
        ),
        migrations.AlterModelOptions(
            name='mailserver',
            options={'ordering': ['-created_at'], 'verbose_name': 'SMTP Server', 'verbose_name_plural': 'SMTP Servers'},
        ),
        migrations.RenameField(
            model_name='mailserver',
            old_name='smtp_port',
            new_name='port',
        ),
        migrations.RenameField(
            model_name='mailserver',
            old_name='smtp_server',
            new_name='server',
        ),
        migrations.RemoveField(
            model_name='mailserver',
            name='email',
        ),
        migrations.RemoveField(
            model_name='mailserver',
            name='login',
        ),
        migrations.RemoveField(
            model_name='mailserver',
            name='password',
        ),
        migrations.AlterField(
            model_name='delivery',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 28, 16, 48, 36, 601401), auto_now_add=True, null=True, verbose_name='\u0414\u0430\u0442\u0430 \u0441\u043e\u0437\u0434\u0430\u043d\u0438\u044f'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='delivery',
            name='name',
            field=models.CharField(default=b'2015-10-28T16:48:36.601190', max_length=128, null=True, verbose_name='\u0418\u043c\u044f \u0440\u0430\u0441\u0441\u044b\u043b\u043a\u0438', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='delivery',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 28, 16, 48, 36, 601435), auto_now=True, null=True, verbose_name='\u0414\u0430\u0442\u0430 \u043e\u0431\u043d\u043e\u0432\u043b\u0435\u043d\u0438\u044f'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='emailfordelivery',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 28, 16, 48, 36, 608269), auto_now_add=True, null=True, verbose_name='\u0414\u0430\u0442\u0430 \u0441\u043e\u0437\u0434\u0430\u043d\u0438\u044f'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='emailfordelivery',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 28, 16, 48, 36, 608300), auto_now=True, null=True, verbose_name='\u0414\u0430\u0442\u0430 \u043e\u0431\u043d\u043e\u0432\u043b\u0435\u043d\u0438\u044f'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='emailmiddledelivery',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 28, 16, 48, 36, 602415), auto_now_add=True, null=True, verbose_name='\u0414\u0430\u0442\u0430 \u0441\u043e\u0437\u0434\u0430\u043d\u0438\u044f'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='emailmiddledelivery',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 28, 16, 48, 36, 602445), auto_now=True, null=True, verbose_name='\u0414\u0430\u0442\u0430 \u043e\u0431\u043d\u043e\u0432\u043b\u0435\u043d\u0438\u044f'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='mailserver',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 28, 16, 48, 36, 600656), auto_now_add=True, null=True, verbose_name='\u0414\u0430\u0442\u0430 \u0441\u043e\u0437\u0434\u0430\u043d\u0438\u044f'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='mailserver',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 28, 16, 48, 36, 600688), auto_now=True, null=True, verbose_name='\u0414\u0430\u0442\u0430 \u043e\u0431\u043d\u043e\u0432\u043b\u0435\u043d\u0438\u044f'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='spamemail',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 28, 16, 48, 36, 609771), auto_now_add=True, null=True, verbose_name='\u0414\u0430\u0442\u0430 \u0441\u043e\u0437\u0434\u0430\u043d\u0438\u044f'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='traceofvisits',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 28, 16, 48, 36, 609118), auto_now_add=True, null=True, verbose_name='\u0414\u0430\u0442\u0430 \u0441\u043e\u0437\u0434\u0430\u043d\u0438\u044f'),
            preserve_default=True,
        ),
    ]
