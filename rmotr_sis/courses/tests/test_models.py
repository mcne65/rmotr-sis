from __future__ import division, unicode_literals, absolute_import

from django.test import TestCase
from django.utils import timezone

from accounts.models import User
from courses.models import Lecture, Course, CourseInstance


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
        course = Course.objects.create(
            name="Advanced Python",
            description="Learn advanced python techniques",
            code="12345")
        professor = User.objects.create(username='professor', is_staff=True)
        instance = CourseInstance.objects.create(
            course=course, professor=professor, lecture_datetime=timezone.now())
        self.assertEqual(CourseInstance.objects.count(), 1)
        self.assertEqual(instance.course.name, "Advanced Python")

    def test_courseinstance_professor_not_staff(self):
        """Should raise AssertionError when professor user is not staff"""
        course = Course.objects.create(
            name="Advanced Python",
            description="Learn advanced python techniques",
            code="12345")
        user = User.objects.create(username='test', is_staff=False)
        with self.assertRaises(AssertionError):
            CourseInstance.objects.create(
                course=course, lecture_datetime=timezone.now(), professor=user)  # user is not staff


class TestLecture(TestCase):

    def setUp(self):
        self.course = Course.objects.create(name="Advanced Python")
        self.professor = User.objects.create(username='professor', is_staff=True)
        self.instance = CourseInstance.objects.create(
            course=self.course, professor=self.professor,
            lecture_datetime=timezone.now())

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
