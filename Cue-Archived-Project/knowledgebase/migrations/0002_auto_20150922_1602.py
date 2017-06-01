# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('knowledgebase', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='questionreviewnote',
            name='question_note_id',
            field=models.ForeignKey(to='knowledgebase.QuestionAnswer'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='questionreviewnote',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='questionanswerflag',
            name='question',
            field=models.ForeignKey(to='knowledgebase.QuestionAnswer'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='questionanswerflag',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='questionanswer',
            name='categories',
            field=models.ManyToManyField(to='knowledgebase.Category'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='questionanswer',
            name='tags',
            field=taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', blank=True, help_text='A comma-separated list of tags.', verbose_name='Tags'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='questionanswer',
            name='topics',
            field=models.ManyToManyField(to='knowledgebase.Topic'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='questionanswer',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='notification',
            name='question',
            field=models.ForeignKey(to='knowledgebase.QuestionAnswer'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='notification',
            name='recipient',
            field=models.ForeignKey(related_name='recipient', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='notification',
            name='sender',
            field=models.ForeignKey(related_name='sender', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='category',
            name='mentors',
            field=models.ManyToManyField(related_name='Mentor', null=True, to=settings.AUTH_USER_MODEL, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='category',
            name='user',
            field=models.ForeignKey(related_name='Author', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
