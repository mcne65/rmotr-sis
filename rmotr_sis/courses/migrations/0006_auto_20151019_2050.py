# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0005_auto_20150904_2309'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courseinstance',
            name='batch',
            field=models.ForeignKey(default=1, to='courses.Batch'),
            preserve_default=False,
        ),
    ]
