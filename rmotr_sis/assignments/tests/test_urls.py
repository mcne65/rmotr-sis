from django.test import TestCase
from django.core.urlresolvers import resolve


class TestAssignmentsURLs(TestCase):

    def test_resolve_assignment_url(self):
        """Should resolve URL into assignments resolve_assignment view"""
        resolver = resolve('/assignments/1')
        self.assertEqual(resolver.view_name, 'assignments:resolve_assignment')
        self.assertEqual(resolver.func.__name__, 'ResolveAssignmentView')
