import uuid
from jsonfield import JSONField

from django.db import models

from rmotr_sis.models import TimeStampedModel
from accounts.models import (TIMEZONE_CHOICES, GENDER_CHOICES,
                             OBJECTIVE_CHOICES, OCCUPATION_CHOICES,
                             EXPERIENCE_CHOICES, AVAILABILITY_CHOICES)
from courses.models import Batch, CourseInstance


class ApplicationReferral(TimeStampedModel):
    name = models.CharField(max_length=30)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Application(TimeStampedModel):

    class Meta:
        unique_together = (('email', 'batch'),)

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    batch = models.ForeignKey(Batch, blank=True, null=True)  # FIXME: this must be required
    status = models.PositiveSmallIntegerField(default=1)
    email_validated = models.BooleanField(default=False)

    # step 1
    email = models.EmailField()
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    # step 2
    gender = models.CharField(max_length=15, choices=GENDER_CHOICES,
                              null=True, blank=True)
    timezone = models.CharField(
        max_length=150, choices=TIMEZONE_CHOICES,
        null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    objective = models.CharField(
        max_length=150, choices=OBJECTIVE_CHOICES,
        null=True, blank=True)
    experience = models.CharField(
        max_length=150, choices=EXPERIENCE_CHOICES,
        null=True, blank=True)
    availability = models.CharField(
        max_length=150, choices=AVAILABILITY_CHOICES,
        null=True, blank=True)
    occupation = models.CharField(
        max_length=150, choices=OCCUPATION_CHOICES,
        null=True, blank=True)
    course_instances = models.ManyToManyField(CourseInstance, blank=True)
    referrals = models.ManyToManyField(ApplicationReferral, blank=True)
    referrals_other = models.CharField(max_length=100, blank=True)

    # step 3
    skills_assessment_questions = JSONField(blank=True, null=False)
    skills_assessment_answers = JSONField(blank=True, null=False)
    skills_assessment_correct_count = models.PositiveSmallIntegerField(blank=True,
                                                                       null=True)

    # step 4 (scholarships)
    need_scholarship = models.BooleanField(default=False)
    scholarship_q1 = models.TextField(max_length=1200, blank=True)
    scholarship_q2 = models.TextField(max_length=1200, blank=True)
    scholarship_q3 = models.TextField(max_length=1200, blank=True)
    scholarship_q4 = models.TextField(max_length=1200, blank=True)
    scholarship_q5 = models.TextField(max_length=1200, blank=True)
    scholarship_q6 = models.TextField(max_length=1200, blank=True)

    def __str__(self):
        return '{} - {}'.format(self.batch, self.email)
