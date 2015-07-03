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
            field=models.CharField(max_length=15, blank=True, null=True, choices=[('male', 'Male'), ('female', 'Female'), ('not-disclosed', 'Prefer not to disclose')]),
        ),
        migrations.AddField(
            model_name='user',
            name='linkedin_profile_url',
            field=models.URLField(max_length=750, blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='objective',
            field=models.CharField(max_length=150, blank=True, null=True, choices=[('get-a-job-as-a-programmer', 'Get a job as a programmer'), ('start-my-own-company', 'Start my own company'), ('get-a-promotion-in-my-current-job', 'Get a promotion in my current job'), ('personal-enrichment', 'Personal enrichment')]),
        ),
        migrations.AddField(
            model_name='user',
            name='occupation',
            field=models.CharField(max_length=150, blank=True, null=True, choices=[('studing-full-time', 'Studing full-time'), ('studing-part-time', 'Studing part-time'), ('unemployed-and-looking-for-job', 'Unemployed and looking for job'), ('unemployed-but-not-looking-for-job', 'Unemployed but not looking for job'), ('self-employeed', 'Self-employeed'), ('working-part-time', 'Working part-time'), ('working-full-time', 'Working full-time')]),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=255, unique=True, verbose_name='email address'),
        ),
    ]
