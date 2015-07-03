from __future__ import division, unicode_literals, absolute_import

import pytz

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify

from rmotr_sis.models import TimeStampedModel

TIMEZONE_CHOICES = tuple([(tz, tz) for tz in pytz.common_timezones])

GENDER_CHOICES = (
    ('male', 'Male'),
    ('female', 'Female'),
    ('not-disclosed', 'Prefer not to disclose'),
)

OBJECTIVE_CHOICES = tuple([(slugify(t), t) for t in ['Get a job as a programmer',
                                                     'Start my own company',
                                                     'Get a promotion in my current job',
                                                     'Personal enrichment']])

OCCUPATION_CHOICES = tuple([(slugify(t), t) for t in ['Studing full-time',
                                                      'Studing part-time',
                                                      'Unemployed and looking for job',
                                                      'Unemployed but not looking for job',
                                                      'Self-employeed',
                                                      'Working part-time',
                                                      'Working full-time']])


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

    # personal information
    birth_date = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=15, choices=GENDER_CHOICES,
                              null=True, blank=True)
    timezone = models.CharField(max_length=150, choices=TIMEZONE_CHOICES,
                                blank=True, null=True)
    objective = models.CharField(max_length=150, choices=OBJECTIVE_CHOICES,
                                 null=True, blank=True)
    occupation = models.CharField(max_length=150, choices=OCCUPATION_CHOICES,
                                  null=True, blank=True)

    # accounts information
    github_handle = models.CharField(max_length=50, blank=True, null=True)
    cloud9_handle = models.CharField(max_length=50, blank=True, null=True)
    twitter_handle = models.CharField(max_length=50, blank=True, null=True)
    linkedin_profile_url = models.URLField(max_length=750, blank=True, null=True)

    last_activity = models.DateTimeField(blank=True, null=True)
