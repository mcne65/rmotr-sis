# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_user_last_activity'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='gender',
            field=models.CharField(blank=True, max_length=10, null=True, choices=[('male', 'Male'), ('female', 'Female')]),
        ),
        migrations.AddField(
            model_name='user',
            name='linkedin_profile_url',
            field=models.URLField(blank=True, max_length=750, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='objective',
            field=models.CharField(blank=True, max_length=150, null=True, choices=[('get-a-job-as-a-programmer', 'Get a job as a programmer'), ('start-my-own-company', 'Start my own company'), ('get-a-promotion-in-my-current-job', 'Get a promotion in my current job'), ('personal-enrichment', 'Personal enrichment')]),
        ),
        migrations.AddField(
            model_name='user',
            name='occupation',
            field=models.CharField(blank=True, max_length=150, null=True, choices=[('studing-full-time', 'Studing full-time'), ('studing-part-time', 'Studing part-time'), ('unemployed-and-looking-for-job', 'Unemployed and looking for job'), ('unemployed-but-not-looking-for-job', 'unemployed but not looking for job'), ('self-employeed', 'Self-employeed'), ('working-part-time', 'Working part-time'), ('working-full-time', 'Working full-time')]),
        ),
    ]
