# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=150, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('code', models.CharField(blank=True, max_length=45, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Lecture',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('subject', models.CharField(max_length=150, null=True)),
                ('date', models.DateField(default=django.utils.timezone.now, verbose_name='Class date')),
                ('notes', models.TextField(blank=True, null=True)),
                ('video_url', models.CharField(blank=True, max_length=200, null=True)),
                ('slides_url', models.CharField(blank=True, max_length=200, null=True)),
                ('summary', models.TextField(blank=True, null=True)),
                ('course', models.ForeignKey(to='courses.Course')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
