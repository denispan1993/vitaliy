# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import re
import django.utils.timezone
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('date_of_birth', models.DateField(null=True, verbose_name='\u0414\u0435\u043d\u044c \u0440\u043e\u0436\u0434\u0435\u043d\u0438\u044f', blank=True)),
                ('gender', models.PositiveSmallIntegerField(default=0, null=True, verbose_name='\u041f\u043e\u043b', blank=True, choices=[(0, '\u041d\u0435 \u043e\u043f\u0440\u0435\u0434\u0435\u043b\u0435\u043d\u043e'), (1, '\u041c\u0443\u0436\u0447\u0438\u043d\u0430'), (2, '\u0416\u0435\u043d\u0449\u0438\u043d\u0430')])),
                ('patronymic', models.CharField(max_length=32, null=True, verbose_name='\u041e\u0442\u0447\u0435\u0441\u0442\u0432\u043e', blank=True)),
                ('settlement', models.CharField(max_length=32, null=True, verbose_name='\u041d\u0430\u0441\u0435\u043b\u0451\u043d\u043d\u044b\u0439 \u043f\u0443\u043d\u043a\u0442', blank=True)),
                ('area', models.CharField(max_length=32, null=True, verbose_name='\u041e\u0431\u043b\u0430\u0441\u0442\u044c', blank=True)),
                ('country', models.CharField(default='\u0423\u043a\u0440\u0430\u0438\u043d\u0430', max_length=32, null=True, verbose_name='\u0421\u0442\u0440\u0430\u043d\u0430', blank=True)),
                ('carrier', models.PositiveSmallIntegerField(default=1, null=True, verbose_name='\u041f\u0435\u0440\u0435\u0432\u043e\u0437\u0447\u0438\u043a', blank=True, choices=[(0, '\u0421\u0430\u043c\u043e\u0432\u044b\u0432\u043e\u0437'), (1, '\u041d\u043e\u0432\u0430\u044f \u043f\u043e\u0447\u0442\u0430'), (2, '\u0423\u043a\u0440\u041f\u043e\u0447\u0442\u0430'), (3, '\u0414\u0435\u043b\u0438\u0432\u0435\u0440\u0438'), (4, '\u0418\u043d\u0422\u0430\u0439\u043c'), (5, '\u041d\u043e\u0447\u043d\u043e\u0439 \u042d\u043a\u0441\u043f\u0440\u0435\u0441\u0441')])),
                ('birthday', models.DateField(null=True, verbose_name='\u0414\u0435\u043d\u044c \u0440\u043e\u0436\u0434\u0435\u043d\u0438\u044f', blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('username', models.CharField(help_text='Required. 32 characters or fewer. Letters, numbers and @/./+/-/_ characters', unique=True, max_length=32, verbose_name='username', validators=[django.core.validators.RegexValidator(re.compile(b'^[\\w.@+-]+$'), 'Enter a valid username.', b'invalid')])),
                ('first_name', models.CharField(max_length=30, verbose_name='first name', blank=True)),
                ('last_name', models.CharField(max_length=30, verbose_name='last name', blank=True)),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions')),
            ],
            options={
                'ordering': ['-created_at'],
                'db_table': 'UserModel',
                'verbose_name': '\u041f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044c',
                'verbose_name_plural': '\u041f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u0438',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.EmailField(max_length=75, verbose_name='email address')),
                ('primary', models.BooleanField(default=False, verbose_name='\u041e\u0441\u043d\u043e\u0432\u043d\u043e\u0439')),
                ('email_delivery_new_products', models.BooleanField(default=True, verbose_name='\u041d\u043e\u0432\u044b\u0435 \u043f\u0440\u043e\u0434\u0443\u043a\u0442\u044b')),
                ('email_delivery_shares_news', models.BooleanField(default=True, verbose_name='\u041d\u043e\u0432\u043e\u0441\u0442\u0438 \u0438 \u0410\u043a\u0446\u0438\u0438')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(related_name='email_parent_user', verbose_name='\u041f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044c', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
                'db_table': 'EmailUserModel',
                'verbose_name': 'Email \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044f',
                'verbose_name_plural': "Email'\u044b \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u0435\u0439",
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Phone',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('phone', models.CharField(max_length=19, verbose_name='\u041d\u043e\u043c\u0435\u0440 \u0442\u0435\u043b\u0435\u0444\u043e\u043d\u0430')),
                ('primary', models.BooleanField(default=False, verbose_name='\u041e\u0441\u043d\u043e\u0432\u043d\u043e\u0439')),
                ('sms_notification', models.BooleanField(default=True, verbose_name='SMS \u0420\u0430\u0441\u0441\u044b\u043b\u043a\u0430')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(related_name='phone_parent_user', verbose_name='\u041f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044c', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
                'db_table': 'PhoneUserModel',
                'verbose_name': '\u0422\u0435\u043b\u0435\u0444\u043e\u043d \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044f',
                'verbose_name_plural': '\u0422\u0435\u043b\u043d\u0444\u043e\u043d\u044b \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u0435\u0439',
            },
            bases=(models.Model,),
        ),
    ]
