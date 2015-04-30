from django.shortcuts import render, get_object_or_404
from .models import Lecture, Course
from django.http import Http404
from django.views.generic import ListView, DetailView


class CourseListView(ListView):
    model = Course
    template_name = 'lectures/course_index.html'
    paginate_by = 20

    def get_queryset(self):
        return Course.objects.order_by("pk")


def class_index(request, course_id):
    try:    
        course = Course.objects.get(pk=course_id)
        lecture_list = course.lecture_set.order_by("pk")
    except Course.DoesnNotExist or Lecture.DoesNotExist:
        lecture_list = None
    context = {'lecture_list':lecture_list, 'course':course}
    return render(request, 'lectures/class_index.html', context)


class ClassDetailView(DetailView):
    model = Lecture
    template_name = 'lectures/class_detail.html'

