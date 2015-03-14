from __future__ import division, unicode_literals, absolute_import

import pytz

from django.db import models

TIMEZONE_CHOICES = tuple([(tz, tz) for tz in pytz.common_timezones])


class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Person(TimeStampedModel):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(max_length=150, unique=True)
    birth_date = models.DateField()
    timezone = models.CharField(max_length=150, choices=TIMEZONE_CHOICES)
    twitter_handle = models.CharField(max_length=50)
    github_handle = models.CharField(max_length=50)
    cloud9_handle = models.CharField(max_length=50)
