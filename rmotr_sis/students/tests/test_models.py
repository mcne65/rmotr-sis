from __future__ import division, unicode_literals, absolute_import

import unittest

from students.models import Person, TIMEZONE_CHOICES


class TestPerson(unittest.TestCase):

    def test_person_create(self):
        """Should create a Person model when all required data is given"""
        Person.objects.create(
            first_name='Pepe',
            last_name='Argento',
            email='pepe@argento.com.ar',
            timezone=TIMEZONE_CHOICES[0][0]
        )
        self.assertEqual(Person.objects.count(), 1)
