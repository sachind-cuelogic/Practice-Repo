# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts_app', '0012_account'),
    ]

    operations = [
        migrations.CreateModel(
            name='BuUnit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('code', models.CharField(max_length=100, null=True, blank=True)),
                ('address', models.CharField(max_length=250)),
                ('email', models.EmailField(max_length=70)),
                ('website', models.URLField(null=True, blank=True)),
                ('is_active', models.BooleanField(default=False)),
                ('plan_start_date', models.DateTimeField(auto_now_add=True)),
                ('plan_end_date', models.DateTimeField(null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.CharField(max_length=100)),
                ('updated_by', models.CharField(max_length=100)),
                ('is_enable', models.BooleanField(default=False)),
                ('account', models.ForeignKey(to='accounts_app.Account', blank=True)),
                ('functional_group', models.ManyToManyField(to='accounts_app.FunctionalGroup', blank=True)),
                ('industry', models.ManyToManyField(to='accounts_app.Industries', blank=True)),
                ('parent_bu_unit', models.ForeignKey(blank=True, to='accounts_app.BuUnit', null=True)),
                ('plans', models.ForeignKey(blank=True, to='accounts_app.Plans', null=True)),
            ],
            options={
                'db_table': 'BuUnit',
            },
        ),
    ]
