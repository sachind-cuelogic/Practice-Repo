# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AssetsManagement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.TextField(null=True, blank=True)),
                ('attachment', models.FileField(null=True, upload_to=b'assets', blank=True)),
                ('cover_photo', models.ImageField(null=True, upload_to=b'assets', blank=True)),
                ('cover_photo_name', models.TextField(null=True, blank=True)),
                ('asset_type', models.CharField(blank=True, max_length=20, null=True, choices=[(1, b'IMAGE'), (2, b'AUDIO'), (3, b'VIDEO')])),
                ('created_by', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'assets_management',
            },
        ),
    ]
