from django.db import models
from students.models import Person, TimeStampedModel


class Lecture(TimeStampedModel):
    subject = models.CharField(max_length=150, blank=False, unique=False, null=True)
    attended = models.ManyToManyField(Person, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    video = models.CharField(max_length=200, blank=True, unique=False, null=True)

    def __str__(self):
        return self.subject





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
