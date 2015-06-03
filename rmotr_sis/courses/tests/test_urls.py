from django.test import TestCase
from django.core.urlresolvers import resolve


class TestCoursesURLs(TestCase):

    def test_course_detail_url(self):
        """Should resolve URL into courses course_detail view"""
        resolver = resolve('/courses/1')
        self.assertEqual(resolver.view_name, 'courses:course_detail')
        self.assertEqual(resolver.func.__name__, 'CourseInstanceDetailView')

    def test_lecture_detail_url(self):
        """Should resolve URL into courses lecture_detail view"""
        resolver = resolve('/courses/lectures/1')
        self.assertEqual(resolver.view_name, 'courses:lecture_detail')
        self.assertEqual(resolver.func.__name__, 'LectureDetailView')
