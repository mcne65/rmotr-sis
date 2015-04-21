from django.test import TestCase
from lectures.models import Lecture
from students.models import Person


class LectureTests(TestCase):

    def test_lecture_was_created(self):
        """Tests whether a lecture object is created."""
        lecture = Lecture(subject="Flask")
        lecture.save()
        self.assertEqual(Lecture.objects.count(), 1)

    def test_students_attended_class(self):
        """Tests whether student(Person) instances are stored as having
        attended a particular lecture"""
        student1 = Person(email="student@gmail.com",
                          first_name="Bob",
                          last_name="Saget")
        student2 = Person(email="student2@gmail.com",
                          first_name="Jim",
                          last_name="Jeffries")
        student1.save()
        student2.save()

        lecture1 = Lecture(subject="functions")
        lecture1.save()

        lecture1.attended.add(student1)
        lecture1.attended.add(student2)

        self.assertIn(student1, lecture1.attended.all())
        self.assertIn(student2, lecture1.attended.all())
        self.assertEqual(lecture1.attended.count(), 2)

