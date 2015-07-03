from __future__ import division, unicode_literals, absolute_import

import pytz

from django.db import models
from django.core import validators
from django.utils.text import slugify
from django.utils import timezone as tz
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin,
                                        UserManager)

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


class User(TimeStampedModel, AbstractBaseUser, PermissionsMixin):

    """Subclass django AbstractBaseUser class to add custom fields

       See django source code here:
          https://github.com/django/django/blob/master/django/contrib/auth/base_user.py#L48
    """

    # authentication fields
    username = models.CharField(
        _('username'),
        max_length=30,
        unique=True,
        help_text=_('Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[
            validators.RegexValidator(
                r'^[\w.@+-]+$',
                _('Enter a valid username. This value may contain only '
                  'letters, numbers ' 'and @/./+/-/_ characters.')
            ),
        ],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    email = models.EmailField(_('email address'), blank=True, unique=True)

    # permissions fields
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )

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

    date_joined = models.DateTimeField(_('date joined'), default=tz.now)
    last_activity = models.DateTimeField(blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
