# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0006_auto_20151029_1721'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='application',
            name='checkout_datetime',
        ),
        migrations.AddField(
            model_name='application',
            name='charge_details',
            field=jsonfield.fields.JSONField(blank=True, default=dict),
        ),
        migrations.AddField(
            model_name='application',
            name='charge_id',
            field=models.CharField(max_length=100, blank=True),
        ),
    ]
