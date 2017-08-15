# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CommentAndVote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'comment_and_vote',
            },
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comment_text', models.TextField(null=True, blank=True)),
                ('user', models.CharField(max_length=100)),
                ('attachment', models.CharField(max_length=126, null=True, blank=True)),
                ('ticket', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('total_like', models.IntegerField(default=0)),
                ('is_active', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'comment',
            },
        ),
        migrations.AddField(
            model_name='commentandvote',
            name='comment',
            field=models.ForeignKey(to='comment_app.Comments'),
        ),
    ]
