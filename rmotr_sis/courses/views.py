from __future__ import division, unicode_literals, absolute_import

from braces.views import LoginRequiredMixin

from django.views.generic import DetailView

from .models import Lecture, CourseInstance


class CourseInstanceDetailView(LoginRequiredMixin, DetailView):
    model = CourseInstance
    template_name = 'courses/course_detail.html'


class LectureDetailView(LoginRequiredMixin, DetailView):
    model = Lecture
    template_name = 'courses/lecture_detail.html'
