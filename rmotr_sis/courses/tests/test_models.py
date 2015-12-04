from __future__ import division, unicode_literals, absolute_import

from datetime import date

from django.test import TestCase
from django.utils import timezone

from accounts.models import User
from courses.models import Batch, Lecture, Course, CourseInstance


class TestCourse(TestCase):

    def test_course_was_created(self):
        """Should create a Course model when given data is valid"""
        course = Course.objects.create(
            name="Advanced Python",
            description="Learn advanced python techniques",
            code="12345")
        self.assertEqual(Course.objects.count(), 1)
        self.assertEqual(course.name, "Advanced Python")


class TestCourseInstance(TestCase):

    def test_courseinstance_was_created(self):
        """Should create a CourseInstance model when given data is valid"""
        batch = Batch.objects.create(number=1, start_date=date.today())
        course = Course.objects.create(
            name="Advanced Python",
            description="Learn advanced python techniques",
            code="12345")

        professor = User(username='professor', email='professor@rmotr.com',
                         is_staff=True)
        professor.set_password('123')
        professor.save()

        instance = CourseInstance.objects.create(
            course=course, professor=professor, lecture_weekday='0',
            batch=batch, lecture_utc_time=timezone.now())
        self.assertEqual(CourseInstance.objects.count(), 1)
        self.assertEqual(instance.course.name, "Advanced Python")


class TestLecture(TestCase):

    def setUp(self):
        self.batch = Batch.objects.create(number=1, start_date=date.today())
        self.course = Course.objects.create(name="Advanced Python")

        self.professor = User(username='professor', email='professor@rmotr.com',
                              is_staff=True)
        self.professor.set_password('123')
        self.professor.save()

        self.instance = CourseInstance.objects.create(
            course=self.course, professor=self.professor, batch=self.batch,
            lecture_utc_time=timezone.now(), lecture_weekday='0')

    def test_lecture_was_created(self):
        """Should create a Lecture model when only required data is given"""
        Lecture.objects.create(title="Flask", course_instance=self.instance)
        self.assertEqual(Lecture.objects.count(), 1)

    def test_lecture_was_created_all_parameters(self):
        """Should create a Lecture model when all fields are given"""
        lecture = Lecture.objects.create(
            title="Flask",
            date=timezone.now(),
            video_url="www.youtube.com",
            slides_url="www.rmotr.com",
            content="The flask framework",
            course_instance=self.instance)
        self.assertEqual(Lecture.objects.count(), 1)
        self.assertIn(lecture.title, "Flask")
