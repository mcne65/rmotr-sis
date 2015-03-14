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

    email = models.EmailField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    timezone = models.CharField(max_length=150, choices=TIMEZONE_CHOICES,
                                blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    twitter_handle = models.CharField(max_length=50, blank=True, null=True)
    github_handle = models.CharField(max_length=50, blank=True, null=True)
    cloud9_handle = models.CharField(max_length=50, blank=True, null=True)

    # legacy
    lg_full_name = models.CharField(max_length=150, blank=True, null=True)
    lg_timezone = models.CharField(max_length=50, blank=True, null=True)

    @property
    def full_name(self):
        if self.first_name and self.last_name:
            return '{0} {1}'.format(self.first_name, self.last_name)
        else:
            return self.lg_full_name

    def __str__(self):
        return self.full_name
