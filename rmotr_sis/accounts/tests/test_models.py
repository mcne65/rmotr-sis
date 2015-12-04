from __future__ import division, unicode_literals, absolute_import

from django.test import TestCase
from django.core.exceptions import ValidationError

from accounts.models import User
from applications.models import Application


class TestUser(TestCase):

    def test_user_create(self):
        """Should create a User model when all required data is given"""
        user = User(username='pepeargento',
                    first_name='Pepe',
                    last_name='Argento',
                    email='pepe@argento.com.ar')
        user.set_password('123')
        user.save()
        self.assertEqual(User.objects.count(), 1)

    def test_user_create_pending_required_data(self):
        """Should not create the User when required fields are pending"""
        with self.assertRaises(ValidationError):
            User.objects.create()
        self.assertEqual(User.objects.count(), 0)

    def test_user_assign_application(self):
        """Should properly link a User with given Application object"""
        user = User(username='pepeargento',
                    first_name='Pepe',
                    last_name='Argento',
                    email='pepe@argento.com.ar')
        user.set_password('123')
        user.save()
        application = Application.objects.create(email='something@rmotr.com')
        user.application = application
        user.save()
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(
            User.objects.get(username='pepeargento').application, application)
