from __future__ import division, unicode_literals, absolute_import

import unittest

from students.models import Profile, TIMEZONE_CHOICES


class TestProfile(unittest.TestCase):

    def test_person_create(self):
        """Should create a Profile model when all required data is given"""
        Profile.objects.create(
            first_name='Pepe',
            last_name='Argento',
            email='pepe@argento.com.ar',
            timezone=TIMEZONE_CHOICES[0][0]
        )
        self.assertEqual(Profile.objects.count(), 1)
