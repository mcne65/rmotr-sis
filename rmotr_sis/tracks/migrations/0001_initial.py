# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('github_repo', models.CharField(max_length=255)),
                ('deleted', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('order', models.PositiveIntegerField()),
                ('deleted', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('order', models.PositiveIntegerField()),
                ('deleted', models.BooleanField(default=False)),
                ('course', models.ForeignKey(to='tracks.Course')),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='AssignmentLesson',
            fields=[
                ('lesson_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='tracks.Lesson')),
                ('source', models.TextField()),
                ('tests', models.TextField()),
            ],
            bases=('tracks.lesson',),
        ),
        migrations.CreateModel(
            name='ReadingLesson',
            fields=[
                ('lesson_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='tracks.Lesson')),
                ('readme', models.TextField()),
            ],
            bases=('tracks.lesson',),
        ),
        migrations.AddField(
            model_name='lesson',
            name='unit',
            field=models.ForeignKey(to='tracks.Unit'),
        ),
        migrations.AddField(
            model_name='course',
            name='track',
            field=models.ForeignKey(to='tracks.Track'),
        ),
    ]
