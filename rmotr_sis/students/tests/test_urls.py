from django.test import TestCase
from django.core.urlresolvers import resolve


class TestStudentsURLs(TestCase):

    def test_student_home_url(self):
        """Should resolve URL into students student_home view"""
        resolver = resolve('/')
        self.assertEqual(resolver.view_name, 'student_home')
        self.assertEqual(resolver.func.__name__, 'StudentHomeView')

    def test_student_list_url(self):
        """Should resolve URL into students student_list view"""
        resolver = resolve('/students/')
        self.assertEqual(resolver.view_name, 'students:student_list')
        self.assertEqual(resolver.func.__name__, 'StudentListView')
