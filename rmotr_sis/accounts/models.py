from __future__ import division, unicode_literals, absolute_import


from django.db import models
from django.core import validators
from django.core.mail import send_mail
from django.utils import timezone as django_timezone
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin,
                                        UserManager)

from rmotr_sis.models import (TimeStampedModel, TIMEZONE_CHOICES, GENDER_CHOICES,
                              OBJECTIVE_CHOICES, OCCUPATION_CHOICES)


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
    email = models.EmailField(_('email address'), max_length=255, unique=True)

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

    date_joined = models.DateTimeField(_('date joined'),
                                       default=django_timezone.now)
    last_activity = models.DateTimeField(blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'username']

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)

    @property
    def has_updated_profile(self):
        """Returns True if the user has already updated some of the profile fields, False otherwise"""
        fields = ['gender', 'timezone', 'birth_date',
                  'github_handle', 'cloud9_handle', 'twitter_handle',
                  'linkedin_profile_url', 'objective', 'occupation']
        return len([f for f in fields if getattr(self, f)]) > 0

    def save(self, *args, **kwargs):
        # force a full validation of all fields before saving
        self.full_clean()
        super(User, self).save(*args, **kwargs)
