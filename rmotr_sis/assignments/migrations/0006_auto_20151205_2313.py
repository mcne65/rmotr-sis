# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assignments', '0005_auto_20150708_1217'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignmentattempt',
            name='pep8_error_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='assignmentattempt',
            name='pep8_output',
            field=models.TextField(null=True, blank=True),
        ),
    ]
