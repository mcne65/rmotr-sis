# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0003_auto_20151021_2114'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='scholarship_a1_email_sent',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='application',
            name='scholarship_a1_solution',
            field=models.URLField(blank=True, max_length=1200),
        ),
        migrations.AddField(
            model_name='application',
            name='scholarship_a2_email_sent',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='application',
            name='scholarship_a2_solution',
            field=models.URLField(blank=True, max_length=1200),
        ),
        migrations.AddField(
            model_name='application',
            name='scholarship_a3_email_sent',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='application',
            name='scholarship_a3_solution',
            field=models.URLField(blank=True, max_length=1200),
        ),
    ]
