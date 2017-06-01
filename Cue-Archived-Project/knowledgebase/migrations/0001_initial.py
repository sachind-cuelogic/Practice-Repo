# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=128)),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('notification_message_index', models.IntegerField()),
                ('viewed', models.BooleanField(default=False)),
                ('notified', models.BooleanField(default=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='QuestionAnswer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('question', models.TextField()),
                ('answer', models.TextField()),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('state', models.IntegerField(default=1)),
                ('difficulty_level', models.IntegerField(default=1)),
                ('is_delete', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name_plural': 'Questions and Answers',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='QuestionAnswerFlag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField()),
                ('date', models.DateField(auto_now_add=True)),
                ('is_delete', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='QuestionReviewNote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_time', models.DateTimeField(auto_now_add=True)),
                ('note', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=128)),
                ('categories', models.ManyToManyField(to='knowledgebase.Category')),
            ],
            options={
                'verbose_name_plural': 'Topics',
            },
            bases=(models.Model,),
        ),
    ]
