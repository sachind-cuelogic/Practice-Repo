# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts_app', '0009_functionalgroup'),
    ]

    operations = [
        migrations.CreateModel(
            name='CrmInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=80, choices=[(b'dynamic_crm', b'DYNAMICCRM'), (b'salesforce', b'SALESFORCE'), (b'service_now', b'SERVICENOW'), (b'siebel', b'SIEBEL')])),
                ('login_url', models.TextField(null=True, blank=True)),
                ('login_body', models.TextField(null=True, blank=True)),
                ('ticket_generate_url', models.TextField(null=True, blank=True)),
                ('ticket_generate_body', models.TextField(null=True, blank=True)),
                ('attachmet_url', models.TextField(null=True, blank=True)),
                ('attachment_body', models.TextField(null=True, blank=True)),
                ('ticket_update_url', models.TextField(null=True, blank=True)),
                ('ticket_update_body', models.TextField(null=True, blank=True)),
                ('ticket_close_url', models.TextField(null=True, blank=True)),
                ('ticket_close_body', models.TextField(null=True, blank=True)),
                ('is_active', models.BooleanField(default=False)),
                ('start_date', models.DateTimeField(null=True, blank=True)),
                ('end_date', models.DateTimeField(null=True, blank=True)),
                ('is_enable', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'crm_information',
            },
        ),
    ]
