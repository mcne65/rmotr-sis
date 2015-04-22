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
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(null=True, max_length=150)),
                ('description', models.TextField(null=True, blank=True)),
                ('code', models.CharField(null=True, max_length=45, blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Lecture',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('subject', models.CharField(null=True, max_length=150)),
                ('date', models.DateField(verbose_name='Class date', default=django.utils.timezone.now)),
                ('notes', models.TextField(null=True, blank=True)),
                ('video_url', models.CharField(null=True, max_length=200, blank=True)),
                ('slides_url', models.CharField(null=True, max_length=200, blank=True)),
                ('summary', models.TextField(null=True, blank=True)),
                ('course', models.ForeignKey(to='lectures.Course', default=1)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
