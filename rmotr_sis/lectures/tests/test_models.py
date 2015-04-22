from django.test import TestCase
from lectures.models import Lecture, Course


class LectureTests(TestCase):

    def test_lecture_was_created(self):
        """Tests whether a lecture object is created."""
        lecture = Lecture(subject="Flask")
        lecture.save()
        self.assertEqual(Lecture.objects.count(), 1)

    def test_lecture_was_created_all_parameters(self):
        """Tests creation of a lecture object with all parameters"""
        import django.utils.timezone as time 

        course = Course(name="Advanced Python")
        course.save()

        lecture = Lecture(
            subject="Flask",
            date=time.now(),
            notes="Notes",
            video_url="www.youtube.com",
            slides_url="www.rmotr.com",
            summary = "The flask framework",
            course=course)

        lecture.save()

        self.assertEqual(Lecture.objects.count(), 1)
        self.assertIn(lecture.subject, "Flask")

