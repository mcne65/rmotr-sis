# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
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
                ('student', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=150, null=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('code', models.CharField(max_length=45, null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CourseInstance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('start_date', models.DateField(null=True, blank=True)),
                ('end_date', models.DateField(null=True, blank=True)),
                ('course', models.ForeignKey(to='courses.Course')),
                ('students', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Lecture',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('subject', models.CharField(max_length=150, null=True)),
                ('date', models.DateField(default=django.utils.timezone.now, verbose_name='Class date')),
                ('notes', models.TextField(null=True, blank=True)),
                ('video_url', models.CharField(max_length=200, null=True, blank=True)),
                ('slides_url', models.CharField(max_length=200, null=True, blank=True)),
                ('summary', models.TextField(null=True, blank=True)),
                ('course_instance', models.ForeignKey(to='courses.CourseInstance')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='assignment',
            name='lecture',
            field=models.ForeignKey(to='courses.Lecture'),
        ),
        migrations.AddField(
            model_name='assignment',
            name='tags',
            field=taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', help_text='A comma-separated list of tags.', verbose_name='Tags'),
        ),
    ]
