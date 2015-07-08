# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assignments', '0004_auto_20150622_1707'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='difficulty',
            field=models.CharField(max_length=4, choices=[('0-VE', 'Very easy'), ('1-E', 'Easy'), ('2-M', 'Medium'), ('3-H', 'Hard'), ('4-VH', 'Very hard')]),
        ),
    ]
