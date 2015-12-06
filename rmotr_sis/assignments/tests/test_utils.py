from django.test import TestCase

from assignments.utils import check_pep8_errors, format_pep8_report


class TestPEP8Utils(TestCase):

    def test_check_pep8_no_errors(self):
        """Should count no errors when a valid pep8 code is given"""
        code = """
import sys
import os

for i in range(10):
    print(i)
"""
        report = check_pep8_errors(code)
        self.assertEqual(report.get_count(), 0)

    def test_check_pep8_errors(self):
        """Should return a Report object with pep8 errors when given code is not pep8 valid"""
        code = """
import sys, os

for i in range(10):
    print(i)

"""
        report = check_pep8_errors(code)
        self.assertEqual(report.get_count(), 2)
        output = format_pep8_report(report)
        self.assertTrue('stdin:2:11: E401 multiple imports on one line' in output)
        self.assertTrue('stdin:6:1: W391 blank line at end of file' in output)
