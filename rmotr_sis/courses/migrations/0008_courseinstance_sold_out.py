# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0007_courseinstance_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='courseinstance',
            name='sold_out',
            field=models.BooleanField(default=False),
        ),
    ]
