# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0002_application_referrals_other'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='need_scholarship',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='application',
            name='scholarship_q1',
            field=models.TextField(blank=True, max_length=1200),
        ),
        migrations.AddField(
            model_name='application',
            name='scholarship_q2',
            field=models.TextField(blank=True, max_length=1200),
        ),
        migrations.AddField(
            model_name='application',
            name='scholarship_q3',
            field=models.TextField(blank=True, max_length=1200),
        ),
        migrations.AddField(
            model_name='application',
            name='scholarship_q4',
            field=models.TextField(blank=True, max_length=1200),
        ),
        migrations.AddField(
            model_name='application',
            name='scholarship_q5',
            field=models.TextField(blank=True, max_length=1200),
        ),
        migrations.AddField(
            model_name='application',
            name='scholarship_q6',
            field=models.TextField(blank=True, max_length=1200),
        ),
    ]
