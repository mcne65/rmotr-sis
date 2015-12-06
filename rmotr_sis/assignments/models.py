from django.db import models

from taggit.managers import TaggableManager

from accounts.models import User
from rmotr_sis.models import TimeStampedModel

DIFFICULTY_CHOICES = (
    ('0-VE', 'Very easy'),
    ('1-E', 'Easy'),
    ('2-M', 'Medium'),
    ('3-H', 'Hard'),
    ('4-VH', 'Very hard'),
)


class Assignment(TimeStampedModel):
    title = models.CharField(max_length=255)
    difficulty = models.CharField(max_length=4, choices=DIFFICULTY_CHOICES)
    source = models.TextField()
    footer = models.TextField()
    solution = models.TextField(blank=True, null=True)

    tags = TaggableManager()

    class Meta:
        ordering = ['difficulty']

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
        count = qs.count()
        if count == 0:
            return 'pending'
        if qs.filter(resolved=True).exists():
            return 'resolved'
        if count == 1 and qs.filter(execution_time=None).exists():
            return 'unsubmitted'
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

    # PEP8 details
    pep8_error_count = models.IntegerField(default=0)
    pep8_output = models.TextField(null=True, blank=True)
