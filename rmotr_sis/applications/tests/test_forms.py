from __future__ import division, unicode_literals, absolute_import

from datetime import date

from django.test import TestCase

from courses.models import Batch
from applications.models import Application
from applications.forms import ApplicationFormStep1


class TestApplicationFormStep1(TestCase):

    def test_form_valid(self):
        """Should validate the form when given data is correct"""
        data = {
            'email': 'm@rmotr.com',
            'first_name': 'Martin',
            'last_name': 'Zugnoni'
        }
        form = ApplicationFormStep1(data)
        self.assertTrue(form.is_valid())

    def test_form_invalid(self):
        """Should not validate when required data is pending"""
        form = ApplicationFormStep1({})
        self.assertFalse(form.is_valid())
        errors = {
            'first_name': ['This field is required.'],
            'last_name': ['This field is required.'],
            'email': ['This field is required.']
        }
        self.assertEqual(form.errors, errors)

    def test_form_email_already_applied(self):
        """Should not validate when given email has already applied for current batch"""
        batch = Batch.objects.create(number=1, start_date=date.today(),
                                     accepting_applications=True)
        Application.objects.create(email='m@rmotr.com', batch=batch)
        data = {
            'email': 'm@rmotr.com',
            'first_name': 'Martin',
            'last_name': 'Zugnoni'
        }
        form = ApplicationFormStep1(data)
        self.assertFalse(form.is_valid())
        errors = {'email': ['This email has already applied in this batch']}
        self.assertEqual(form.errors, errors)
