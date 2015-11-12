# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0006_auto_20151019_2050'),
    ]

    operations = [
        migrations.AddField(
            model_name='courseinstance',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
