# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts_app', '0006_auto_20170803_1105'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='industries',
        ),
        migrations.RemoveField(
            model_name='account',
            name='plans',
        ),
        migrations.RemoveField(
            model_name='product',
            name='category',
        ),
        migrations.RemoveField(
            model_name='product',
            name='organization',
        ),
        migrations.DeleteModel(
            name='Account',
        ),
        migrations.DeleteModel(
            name='Category',
        ),
        migrations.DeleteModel(
            name='Industries',
        ),
        migrations.DeleteModel(
            name='Plans',
        ),
        migrations.DeleteModel(
            name='Product',
        ),
    ]
