# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0001_initial'),
        ('students', '0001_initial'),
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('difficulty', models.CharField(max_length=2, choices=[('VE', 'Very easy'), ('E', 'Easy'), ('M', 'Medium'), ('H', 'Hard'), ('VH', 'Very hard')])),
                ('source', models.TextField()),
                ('footer', models.TextField()),
                ('lecture', models.ForeignKey(to='courses.Lecture')),
                ('tags', taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', help_text='A comma-separated list of tags.', verbose_name='Tags')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AssignmentAttempt',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('source', models.TextField()),
                ('start_datetime', models.DateTimeField()),
                ('end_datetime', models.DateTimeField(null=True, blank=True)),
                ('output', models.TextField(null=True, blank=True)),
                ('errors', models.TextField(null=True, blank=True)),
                ('execution_time', models.FloatField(null=True, blank=True)),
                ('resolved', models.BooleanField(default=False)),
                ('assignment', models.ForeignKey(to='courses.Assignment')),
                ('student', models.ForeignKey(to='students.Profile')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
