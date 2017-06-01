# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('ppiauth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('user', models.OneToOneField(primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('first_name', models.CharField(max_length=50, blank=True)),
                ('last_name', models.CharField(max_length=50, blank=True)),
                ('user_type', models.CharField(default=b'Normal User', max_length=50, blank=True, choices=[(b'Administrator', b'ADMINISTRATOR'), (b'Mentor', b'MENTOR'), (b'Normal User', b'NORMAL USER')])),
                ('designation', models.CharField(max_length=120, blank=True)),
                ('about', models.TextField(null=True, blank=True)),
                ('gender', models.CharField(blank=True, max_length=20, choices=[(b'Female', b'FEMALE'), (b'Male', b'MALE')])),
                ('dob', models.DateField(null=True, blank=True)),
                ('profile_picture', models.ImageField(null=True, upload_to=b'profile_picture/', blank=True)),
                ('profile_picture_icon', django_resized.forms.ResizedImageField(null=True, upload_to=b'profile_picture/', blank=True)),
                ('profile_picture_thumbnail', django_resized.forms.ResizedImageField(null=True, upload_to=b'profile_picture/', blank=True)),
                ('profile_picture_macroicon', django_resized.forms.ResizedImageField(null=True, upload_to=b'profile_picture/', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
