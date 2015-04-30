from django.test import TestCase
from courses.models import Lecture, Course



class CourseTests(TestCase):

    def test_course_was_created(self):
        """Tests whether a course object is created"""
        course = Course.objects.create(name="Advanced Python",
                                       description="Learn advanced python techniques",
                                       code="12345")
        self.assertEqual(Course.objects.count(),1)
        self.assertEqual(course.name, "Advanced Python")



class LectureTests(TestCase):

    def test_lecture_was_created(self):
        """Tests whether a lecture object is created."""
        course = Course.objects.create(name="Advanced Python")
        lecture = Lecture.objects.create(subject="Flask", course=course)
        self.assertEqual(Lecture.objects.count(), 1)

    def test_lecture_was_created_all_parameters(self):
        """Tests creation of a lecture object with all parameters"""
        import django.utils.timezone as time 

        course = Course.objects.create(name="Advanced Python")

        lecture = Lecture.objects.create(
            subject="Flask",
            date=time.now(),
            notes="Notes",
            video_url="www.youtube.com",
            slides_url="www.rmotr.com",
            summary = "The flask framework",
            course=course)

        self.assertEqual(Lecture.objects.count(), 1)
        self.assertIn(lecture.subject, "Flask")

