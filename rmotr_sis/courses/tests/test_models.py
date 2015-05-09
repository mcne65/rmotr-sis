from __future__ import division, unicode_literals, absolute_import

from django.test import TestCase
from django.utils import timezone as time

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
        instance = CourseInstance.objects.create(course=course)
        self.assertEqual(CourseInstance.objects.count(), 1)
        self.assertEqual(instance.course.name, "Advanced Python")


class TestLecture(TestCase):

    def setUp(self):
        self.course = Course.objects.create(name="Advanced Python")
        self.instance = CourseInstance.objects.create(course=self.course)

    def test_lecture_was_created(self):
        """Should create a Lecture model when only required data is given"""
        Lecture.objects.create(subject="Flask", course_instance=self.instance)
        self.assertEqual(Lecture.objects.count(), 1)

    def test_lecture_was_created_all_parameters(self):
        """Should create a Lecture model when all fields are given"""
        lecture = Lecture.objects.create(
            subject="Flask",
            date=time.now(),
            notes="Notes",
            video_url="www.youtube.com",
            slides_url="www.rmotr.com",
            summary="The flask framework",
            course_instance=self.instance)
        self.assertEqual(Lecture.objects.count(), 1)
        self.assertIn(lecture.subject, "Flask")
