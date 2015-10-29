# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0005_application_utm_source'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='checkout_datetime',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='application',
            name='selected',
            field=models.BooleanField(default=False),
        ),
    ]
