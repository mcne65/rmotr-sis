from django.db import models

from taggit.managers import TaggableManager

from accounts.models import User
from rmotr_sis.models import TimeStampedModel

DIFFICULTY_CHOICES = (
    ('VE', 'Very easy'),
    ('E', 'Easy'),
    ('M', 'Medium'),
    ('H', 'Hard'),
    ('VH', 'Very hard'),
)


class Assignment(TimeStampedModel):
    title = models.CharField(max_length=255)
    difficulty = models.CharField(max_length=2, choices=DIFFICULTY_CHOICES)
    source = models.TextField()
    footer = models.TextField()
    solution = models.TextField(blank=True, null=True)

    tags = TaggableManager()

    def __str__(self):
        return self.title

    @property
    def tag_list(self):
        return [t.name for t in self.tags.all()]

    def get_status(self, student):
        """Returns the assignment status (pending, failed, resolved)
           for certain student.
        """
        qs = AssignmentAttempt.objects.filter(student=student, assignment=self)
        if qs.count() == 0:
            return 'pending'
        qs = qs.filter(resolved=True)
        if qs.exists():
            return 'resolved'
        return 'failed'

    def get_attempts(self, student):
        """Returns the amount of attempts the student executed for
           this assignment.
        """
        return AssignmentAttempt.objects.filter(
            student=student, assignment=self).exclude(end_datetime=None).count()


class AssignmentAttempt(TimeStampedModel):
    assignment = models.ForeignKey(Assignment)
    student = models.ForeignKey(User)
    student_source = models.TextField()
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField(null=True, blank=True)
    resolved = models.BooleanField(default=False)

    # execution details
    source = models.TextField()
    output = models.TextField(null=True, blank=True)
    errors = models.TextField(null=True, blank=True)
    execution_time = models.FloatField(null=True, blank=True)
