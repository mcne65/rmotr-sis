from __future__ import division, unicode_literals, absolute_import

from taggit.managers import TaggableManager

from django.db import models
from django.utils import timezone

from accounts.models import User
from rmotr_sis.models import TimeStampedModel

DIFFICULTY_CHOICES = (
    ('VE', 'Very easy'),
    ('E', 'Easy'),
    ('M', 'Medium'),
    ('H', 'Hard'),
    ('VH', 'Very hard'),
)


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
    students = models.ManyToManyField(User)

    def __str__(self):
        return '{} ({} - {})'.format(self.course.name,
                                     self.start_date, self.end_date)


class Lecture(TimeStampedModel):
    course_instance = models.ForeignKey(CourseInstance)
    title = models.CharField(max_length=150)
    date = models.DateField(default=timezone.now)
    content = models.TextField(blank=True, null=True)
    video_url = models.CharField(max_length=500, blank=True, null=True)
    slides_url = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.title


class Assignment(TimeStampedModel):
    title = models.CharField(max_length=255)
    lecture = models.ForeignKey(Lecture)
    difficulty = models.CharField(max_length=2, choices=DIFFICULTY_CHOICES)
    source = models.TextField()
    footer = models.TextField()
    solution = models.TextField(blank=True, null=True)

    tags = TaggableManager()

    def __str__(self):
        return '{} ({})'.format(
            ', '.join([t.name for t in self.tags.all()]),
            self.difficulty
        )

    def is_resolved_by_student(self, student):
        """Returns True if the student has already resolved the assignment,
           or False otherwise
        """
        return AssignmentAttempt.objects.filter(
            student=student, assignment=self, resolved=True).exists()


class AssignmentAttempt(TimeStampedModel):
    assignment = models.ForeignKey(Assignment)
    student = models.ForeignKey(User)
    source = models.TextField()
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField(null=True, blank=True)
    output = models.TextField(null=True, blank=True)
    errors = models.TextField(null=True, blank=True)
    execution_time = models.FloatField(null=True, blank=True)
    resolved = models.BooleanField(default=False)
