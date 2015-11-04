# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0007_auto_20151029_2215'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='application',
            options={'ordering': ['modified']},
        ),
        migrations.AddField(
            model_name='application',
            name='custom_price_in_cents',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
