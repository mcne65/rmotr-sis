# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assignments', '0002_assignmentattempt_student_source'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='assignment',
            options={'ordering': ['difficulty']},
        ),
        migrations.AlterField(
            model_name='assignment',
            name='difficulty',
            field=models.CharField(choices=[('VE', 'Very easy'), ('E', 'Easy'), ('M', 'Medium'), ('H', 'Hard'), ('VH', 'Very hard')], max_length=4),
        ),
    ]
