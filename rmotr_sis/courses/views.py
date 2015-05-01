from __future__ import division, unicode_literals, absolute_import

from braces.views import LoginRequiredMixin

from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404

from .models import Lecture, Course


class CourseListView(LoginRequiredMixin, ListView):
    model = Course
    template_name = 'courses/course_index.html'
    paginate_by = 20

    def get_queryset(self):
        return Course.objects.order_by("pk")


class LectureListView(LoginRequiredMixin, ListView):
    model = Lecture
    template_name = 'courses/lecture_index.html'

    def get_queryset(self):
        course = get_object_or_404(Course, pk=self.kwargs['course_id'])
        return course.lecture_set.order_by("pk")


class LectureDetailView(LoginRequiredMixin, DetailView):
    model = Lecture
    template_name = 'courses/lecture_detail.html'
