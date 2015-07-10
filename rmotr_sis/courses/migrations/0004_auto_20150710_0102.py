# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
from django.conf import settings
import datetime


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('courses', '0003_courseinstance__code'),
    ]

    operations = [
        migrations.AddField(
            model_name='courseinstance',
            name='lecture_datetime',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 10, 1, 1, 52, 538239, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='courseinstance',
            name='professor',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='courseinstance_professor_set', default=1),
            preserve_default=False,
        ),
    ]
