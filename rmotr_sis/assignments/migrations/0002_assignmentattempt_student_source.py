# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assignments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignmentattempt',
            name='student_source',
            field=models.TextField(default='pass'),
            preserve_default=False,
        ),
    ]
