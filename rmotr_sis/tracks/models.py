import uuid
from django.db import models
from extended_choices import Choices


LESSON_TYPES = Choices(
    ('ASSIGNMENT',  'assignment', 'Assignment'),
    ('READING',   'reading', 'Reading'),
)


class Track(models.Model):
    name = models.CharField(max_length=64)


class Course(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    track = models.ForeignKey(Track)
    name = models.CharField(max_length=255)
    github_repo = models.CharField(max_length=255)
    deleted = models.BooleanField(default=False)


class Unit(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course = models.ForeignKey(Course)
    name = models.CharField(max_length=255)
    order = models.PositiveIntegerField()
    last_commit_hash = models.CharField(max_length=40)
    deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ['order']

    def __unicode__(self):
        return self.name


class Lesson(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    unit = models.ForeignKey(Unit)
    name = models.CharField(max_length=255)
    order = models.PositiveIntegerField()
    last_commit_hash = models.CharField(max_length=40)
    deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ['order']

    @property
    def type(self):
        if hasattr(self, 'assignmentlesson'):
            return LESSON_TYPES.ASSIGNMENT
        elif hasattr(self, 'readinglesson'):
            return LESSON_TYPES.READING

    def __unicode__(self):
        return self.name


class ReadingLesson(Lesson):
    readme = models.TextField()


class AssignmentLesson(Lesson):
    source = models.TextField()
    tests = models.TextField()


# class LessonUserStatus(models.Model):
#     user = models.ForeignKey(User)
#     lesson = models.ForeignKey(Lesson)
#     start_datetime = models.DateTimeField(null=True, blank=True)
#     end_datetime = models.DateTimeField(null=True, blank=True)


# class AssignmentAttempt(models.Model):
#     user = models.ForeignKey(User)
#     assignment = models.ForeignKey(AssignmentLesson)
#     resolved = models.BooleanField(default=False)

#     # execution details
#     source = models.TextField()
#     output = models.TextField(null=True, blank=True)
#     errors = models.TextField(null=True, blank=True)
#     execution_time = models.FloatField(null=True, blank=True)

#     # PEP8 details
#     pep8_error_count = models.IntegerField(default=0)
#     pep8_output = models.TextField(null=True, blank=True)
