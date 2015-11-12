# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20150703_1500'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='occupation',
            field=models.CharField(blank=True, max_length=150, null=True, choices=[('studing-full-time', 'Studing full-time'), ('studing-part-time', 'Studing part-time'), ('unemployed-and-looking-for-job', 'Unemployed and looking for job'), ('unemployed-but-not-looking-for-job', 'Unemployed but not looking for job'), ('self-employeed', 'Self-employeed'), ('working-part-time', 'Working part-time'), ('working-full-time', 'Working full-time'), ('both-working-and-studing', 'Both working and studing')]),
        ),
    ]
