# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts_app', '0015_product'),
    ]

    operations = [
        migrations.CreateModel(
            name='UsageInformation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_active', models.BooleanField(default=False)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField(null=True, blank=True)),
                ('bu_unit', models.ForeignKey(to='accounts_app.BuUnit')),
                ('functional_group', models.ForeignKey(to='accounts_app.FunctionalGroup')),
            ],
            options={
                'db_table': 'usage_information',
            },
        ),
    ]
