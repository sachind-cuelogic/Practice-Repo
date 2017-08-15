# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('id', models.UUIDField(serialize=False, primary_key=True)),
                ('email', models.EmailField(unique=True, max_length=254)),
                ('full_name', models.CharField(max_length=80, null=True, blank=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
                ('is_email_verified', models.BooleanField(default=False)),
                ('username', models.CharField(max_length=50, null=True, blank=True)),
                ('cordis_username', models.CharField(max_length=50, null=True, blank=True)),
                ('cordis_access_token', models.CharField(max_length=70, null=True, blank=True)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('country_code', models.CharField(max_length=6, null=True, blank=True)),
                ('phone_number', models.CharField(blank=True, max_length=15, null=True, validators=[django.core.validators.RegexValidator(regex=b'^\\+?1?\\d{9,15}$', message=b"Phone number must be entered in the format:'         ' '+999999999'. Up to 15 digits allowed.")])),
                ('role', models.CharField(default=b'Normal User', max_length=50, null=True, choices=[(b'Agent', b'AGENT'), (b'Normal User', b'NORMAL USER')])),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
