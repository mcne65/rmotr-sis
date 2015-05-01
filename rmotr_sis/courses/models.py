from __future__ import division, unicode_literals, absolute_import

from django.db import models
from django.utils import timezone

from students.models import TimeStampedModel, Profile


class Course(TimeStampedModel):
    name = models.CharField(max_length=150, blank=False, null=True)
    description = models.TextField(blank=True, null=True)
    code = models.CharField(max_length=45, blank=True, null=True)

    def __str__(self):
        return self.name


class CourseInstance(TimeStampedModel):
    course = models.ForeignKey(Course)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    students = models.ManyToManyField(Profile)

    def __str__(self):
        return '{} ({} - {})'.format(self.course.name,
                                     self.start_date, self.end_date)


class Lecture(TimeStampedModel):
    subject = models.CharField(max_length=150, blank=False,
                               unique=False, null=True)
    date = models.DateField('Class date', default=timezone.now)
    notes = models.TextField(blank=True, null=True)
    video_url = models.CharField(max_length=200, blank=True,
                                 unique=False, null=True)
    slides_url = models.CharField(max_length=200, blank=True,
                                  unique=False, null=True)
    summary = models.TextField(blank=True, null=True)
    course_instance = models.ForeignKey(CourseInstance)

    @property
    def lecture_handle(self):
        if self.subject and self.date:
            return "{0} [{1}]".format(self.subject, self.date)
        else:
            return self.subject

    def __str__(self):
        return self.lecture_handle
