# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0008_auto_20151104_0136'),
        ('accounts', '0004_auto_20151112_1921'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='application',
            field=models.ForeignKey(blank=True, to='applications.Application', null=True),
        ),
    ]
