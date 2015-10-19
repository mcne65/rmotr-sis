from collections import OrderedDict

from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

from accounts.models import User
from rmotr_sis.models import TimeStampedModel
from assignments.models import Assignment

WEEKDAY_CHOICES = (
    ('0', 'Monday'),
    ('1', 'Tuesday'),
    ('2', 'Wednesday'),
    ('3', 'Thursday'),
    ('4', 'Friday'),
    ('5', 'Saturday'),
    ('6', 'Sunday'),
)


def validate_is_professor(value):
    try:
        professor = User.objects.get(id=value)
    except User.DoesNotExist:
        raise ValidationError('Professor user does not exist')

    if not professor.is_staff:
        raise ValidationError('Professor user must be staff')


class Batch(TimeStampedModel):
    number = models.PositiveSmallIntegerField()
    start_date = models.DateField()
    comments = models.TextField(blank=True, null=False)
    accepting_applications = models.BooleanField(default=False)

    def __str__(self):
        return 'Batch {}'.format(self.number)

    @classmethod
    def get_current_batch(cls):
        return cls.objects.filter(accepting_applications=True).first() or None

    def save(self):
        count = Batch.objects.filter(accepting_applications=True).count()
        if count and self.accepting_applications:
            raise ValidationError('Only one batch must be accepting '
                                  'applications at the same time')
        super(Batch, self).save()


class Course(TimeStampedModel):
    name = models.CharField(max_length=150, blank=False, null=True)
    description = models.TextField(blank=True, null=True)
    code = models.CharField(max_length=45, blank=True, null=True)

    def __str__(self):
        return self.name


class CourseInstance(TimeStampedModel):
    course = models.ForeignKey(Course)
    batch = models.ForeignKey(Batch, blank=True, null=True)  # FIXME: this must be required after migrations
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    professor = models.ForeignKey(User, related_name='courseinstance_professor_set',
                                  validators=[validate_is_professor])
    lecture_weekday = models.CharField(max_length=1, choices=WEEKDAY_CHOICES)
    lecture_utc_time = models.TimeField()
    students = models.ManyToManyField(User, blank=True)
    _code = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return '#{} - {} ({} - {})'.format(
            self.code, self.course.name, self.start_date, self.end_date)

    @property
    def code(self):
        return '{}-{}'.format(self.course.code, self._code)

    def is_student(self, student):
        """Returns True if the student is participating in this course
           instance, or False otherwise.
        """
        return student in self.students.all()


class Lecture(TimeStampedModel):
    course_instance = models.ForeignKey(CourseInstance)
    title = models.CharField(max_length=150)
    date = models.DateField(default=timezone.now)
    content = models.TextField(blank=True, null=True)
    video_url = models.CharField(max_length=500, blank=True, null=True)
    slides_url = models.CharField(max_length=500, blank=True, null=True)
    assignments = models.ManyToManyField(Assignment, blank=True)
    published = models.BooleanField(default=False)

    def get_assignments_for_user(self, user):
        assignments = self.assignments.all()
        for a in assignments:
            a.status = a.get_status(user)
            a.attempts = a.get_attempts(user)
        return assignments

    def __str__(self):
        return self.title

    def get_assignment_summary(self):
        """"Returns all assignments per student with the current
            assignment status.
        """
        summary = OrderedDict()
        students = self.course_instance.students.all()
        assignments = self.assignments.all()
        for student in students:
            summary.setdefault(student, OrderedDict())
            for a in assignments:
                summary[student][a] = a.get_status(student)
        return summary
