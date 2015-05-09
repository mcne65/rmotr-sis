from __future__ import division, unicode_literals, absolute_import

import unittest

from accounts.models import User, TIMEZONE_CHOICES


class TestUser(unittest.TestCase):

    def test_person_create(self):
        """Should create a User model when all required data is given"""
        User.objects.create(
            first_name='Pepe',
            last_name='Argento',
            email='pepe@argento.com.ar',
            timezone=TIMEZONE_CHOICES[0][0]
        )
        self.assertEqual(User.objects.count(), 1)
