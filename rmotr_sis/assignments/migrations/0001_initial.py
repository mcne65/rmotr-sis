# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('taggit', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=255)),
                ('difficulty', models.CharField(max_length=2, choices=[('VE', 'Very easy'), ('E', 'Easy'), ('M', 'Medium'), ('H', 'Hard'), ('VH', 'Very hard')])),
                ('source', models.TextField()),
                ('footer', models.TextField()),
                ('solution', models.TextField(null=True, blank=True)),
                ('tags', taggit.managers.TaggableManager(verbose_name='Tags', help_text='A comma-separated list of tags.', to='taggit.Tag', through='taggit.TaggedItem')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AssignmentAttempt',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('source', models.TextField()),
                ('start_datetime', models.DateTimeField()),
                ('end_datetime', models.DateTimeField(null=True, blank=True)),
                ('output', models.TextField(null=True, blank=True)),
                ('errors', models.TextField(null=True, blank=True)),
                ('execution_time', models.FloatField(null=True, blank=True)),
                ('resolved', models.BooleanField(default=False)),
                ('assignment', models.ForeignKey(to='assignments.Assignment')),
                ('student', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
