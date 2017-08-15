# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts_app', '0004_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('is_active', models.BooleanField(default=False)),
                ('attachments', models.ImageField(null=True, upload_to=b'products', blank=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.CharField(max_length=100)),
                ('updated_by', models.CharField(max_length=100)),
                ('total_reported_issues', models.IntegerField(default=0)),
                ('total_resolved_issues', models.IntegerField(default=0)),
                ('total_resolved_ticket_heat_index', models.IntegerField(default=0)),
                ('average_resolved_ticket_heat_index', models.FloatField(default=0)),
                ('category', models.ForeignKey(to='accounts_app.Category')),
                ('organization', models.ForeignKey(to='accounts_app.Account')),
            ],
            options={
                'db_table': 'product',
            },
        ),
    ]
