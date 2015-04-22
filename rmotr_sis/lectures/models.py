from django.db import models
from students.models import Person, TimeStampedModel
from django.utils import timezone


class Course(TimeStampedModel):

    name = models.CharField(max_length=150, blank=False, null=True)
    description = models.TextField(blank=True, null=True)
    code = models.CharField(max_length=45, blank=True, null=True)

    def __str__(self):
        return self.name

class Lecture(TimeStampedModel):
    #subject may be represented as a many-to-many relationship with another table
    #for subjects.
    subject = models.CharField(max_length=150, blank=False, unique=False, null=True)
    date = models.DateField('Class date', default=timezone.now)
    notes = models.TextField(blank=True, null=True)
    video_url = models.CharField(max_length=200, blank=True, unique=False, null=True)
    slides_url = models.CharField(max_length=200, blank=True, unique=False, null=True)
    summary = models.TextField(blank=True, null=True)
    course = models.ForeignKey('Course', default=1) 

    @property
    def lecture_handle(self):
        if self.subject and self.date:
            return "{0} [{1}]".format(self.subject, self.date)
        else:
            return self.subject
    
    def __str__(self):
        return self.lecture_handle





"""
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

class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
"""
