from __future__ import division, unicode_literals, absolute_import

import pytz

from django.contrib.auth.models import AbstractUser
from django.db import models

from rmotr_sis.models import TimeStampedModel

TIMEZONE_CHOICES = tuple([(tz, tz) for tz in pytz.common_timezones])


class User(TimeStampedModel, AbstractUser):

    """Subclass django default AbstractUser class to add custom fields

       All basic fields [1] are alredy provided by AbstractUser class, see
       django source code in [2].

       [1] inherited fields
            # username
            # first_name
            # last_name
            # email
            # is_staff
            # is_active
            # date_joined
            # last_login

       [2] AbstractUser code
            # https://github.com/django/django/blob/master/django/contrib/auth/models.py#L288
    """

    birth_date = models.DateField(blank=True, null=True)
    twitter_handle = models.CharField(max_length=50, blank=True, null=True)
    github_handle = models.CharField(max_length=50, blank=True, null=True)
    cloud9_handle = models.CharField(max_length=50, blank=True, null=True)
    timezone = models.CharField(max_length=150, choices=TIMEZONE_CHOICES,
                                blank=True, null=True)
    last_activity = models.DateTimeField(blank=True, null=True)
