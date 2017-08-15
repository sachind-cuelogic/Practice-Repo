# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserBadgeCount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.CharField(max_length=100)),
                ('badge_count', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'user_badge_count',
            },
        ),
        migrations.CreateModel(
            name='UserNotifications',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.CharField(max_length=100)),
                ('notification_text', models.TextField(null=True, blank=True)),
                ('notification_param', models.CharField(max_length=1000, null=True, blank=True)),
                ('reported_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('is_read', models.BooleanField(default=False)),
                ('notification_type', models.CharField(max_length=50, null=True, choices=[(b'System_Generated', b'SYSTEM GENERATED'), (b'User_Owned', b'USER OWNED'), (b'component_failure', b'COMPONENT FAILURE'), (b'user_offers', b'USER OFFERS'), (b'user_scenarios', b'USER SCENARIOS')])),
            ],
            options={
                'db_table': 'user_notification',
            },
        ),
    ]
