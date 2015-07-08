# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_lecture_published'),
    ]

    operations = [
        migrations.AddField(
            model_name='courseinstance',
            name='_code',
            field=models.CharField(max_length=10, blank=True),
        ),
    ]
