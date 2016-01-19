# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='last_commit_hash',
            field=models.CharField(default='', max_length=40),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='unit',
            name='last_commit_hash',
            field=models.CharField(default='', max_length=40),
            preserve_default=False,
        ),
    ]
