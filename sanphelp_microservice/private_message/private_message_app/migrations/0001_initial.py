# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('message_text', models.TextField(null=True, blank=True)),
                ('attachment', models.FileField(null=True, upload_to=b'', blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('ticket', models.CharField(max_length=10, null=True, blank=True)),
                ('from_user_read', models.BooleanField(default=True)),
                ('to_user_read', models.BooleanField(default=False)),
                ('from_user_delete', models.BooleanField(default=False)),
                ('to_user_delete', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'message',
            },
        ),
    ]
