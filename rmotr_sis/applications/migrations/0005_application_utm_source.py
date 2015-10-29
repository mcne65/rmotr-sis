# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0004_auto_20151022_2307'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='utm_source',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
