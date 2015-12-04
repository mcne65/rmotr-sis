from __future__ import division, unicode_literals, absolute_import

import pytz

from django.utils.text import slugify
from django.db import models

TIMEZONE_CHOICES = tuple([(tz, tz) for tz in pytz.common_timezones])

GENDER_CHOICES = (
    ('male', 'Male'),
    ('female', 'Female'),
    ('not-disclosed', 'Prefer not to disclose'),
)

OBJECTIVE_CHOICES = tuple([(slugify(t), t) for t in [
    'Get a job as a programmer',
    'Start my own company',
    'Get a promotion in my current job',
    'Personal enrichment'
]])

OCCUPATION_CHOICES = tuple([(slugify(t), t) for t in [
    'Studing full-time',
    'Studing part-time',
    'Unemployed and looking for job',
    'Unemployed but not looking for job',
    'Self-employeed',
    'Working part-time',
    'Working full-time',
    'Both working and studing'
]])

EXPERIENCE_CHOICES = tuple([(slugify(t), t) for t in [
    'Never studied before',
    'Less than 1 month',
    'Between 1 and 3 months',
    'Between 3 and 6 months',
    'Between 6 and 12 months',
    'Between 1 and 2 years',
    'More than 2 years'
]])

AVAILABILITY_CHOICES = tuple([(slugify(t), t) for t in [
    'Less than 10hours/week',
    '20hours/week',
    '30hours/week',
    '40hours/week',
    '50hours/week',
    '60hours/week',
    '70hours/week',
]])


class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
