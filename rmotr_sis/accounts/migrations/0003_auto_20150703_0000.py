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
            field=models.CharField(choices=[('male', 'Male'), ('female', 'Female'), ('not-disclosed', 'Prefer not to disclose')], blank=True, max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='linkedin_profile_url',
            field=models.URLField(null=True, max_length=750, blank=True),
        ),
        migrations.AddField(
            model_name='user',
            name='objective',
            field=models.CharField(choices=[('get-a-job-as-a-programmer', 'Get a job as a programmer'), ('start-my-own-company', 'Start my own company'), ('get-a-promotion-in-my-current-job', 'Get a promotion in my current job'), ('personal-enrichment', 'Personal enrichment')], blank=True, max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='occupation',
            field=models.CharField(choices=[('studing-full-time', 'Studing full-time'), ('studing-part-time', 'Studing part-time'), ('unemployed-and-looking-for-job', 'Unemployed and looking for job'), ('unemployed-but-not-looking-for-job', 'Unemployed but not looking for job'), ('self-employeed', 'Self-employeed'), ('working-part-time', 'Working part-time'), ('working-full-time', 'Working full-time')], blank=True, max_length=150, null=True),
        ),
    ]
