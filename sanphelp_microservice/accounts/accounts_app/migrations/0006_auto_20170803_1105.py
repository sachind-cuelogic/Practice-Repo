# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts_app', '0005_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='organization',
            field=models.CharField(max_length=100),
        ),
    ]
