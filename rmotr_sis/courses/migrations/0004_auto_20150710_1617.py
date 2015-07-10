# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import courses.models
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
            name='lecture_utc_time',
            field=models.TimeField(default=datetime.datetime(2015, 7, 10, 16, 17, 10, 516869, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='courseinstance',
            name='lecture_weekday',
            field=models.CharField(choices=[('0', 'Monday'), ('1', 'Tuesday'), ('2', 'Wednesday'), ('3', 'Thursday'), ('4', 'Friday'), ('5', 'Saturday'), ('6', 'Sunday')], default='0', max_length=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='courseinstance',
            name='professor',
            field=models.ForeignKey(default=1, related_name='courseinstance_professor_set', to=settings.AUTH_USER_MODEL, validators=[courses.models.validate_is_professor]),
            preserve_default=False,
        ),
    ]
