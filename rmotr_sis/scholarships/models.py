import uuid

from django.db import models

from accounts.models import (TIMEZONE_CHOICES, GENDER_CHOICES,
                             OBJECTIVE_CHOICES, OCCUPATION_CHOICES,
                             EXPERIENCE_CHOICES, AVAILABILITY_CHOICES)
from courses.models import CourseInstance

APPLICATION_STATUS_CHOICES = (
    ('1', '1 - Personal information completed'),
    ('2', '2 - Academic information completed'),
    ('3', '3 - Skills assessment approved'),
)


class ScholarshipApplication(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    status = models.CharField(max_length=1, choices=APPLICATION_STATUS_CHOICES,
                              default=APPLICATION_STATUS_CHOICES[0][0])
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
    course_instances = models.ManyToManyField(CourseInstance,
                                              null=True, blank=True)

    # step 3
    skills_assessment_approved = models.BooleanField(default=False)
