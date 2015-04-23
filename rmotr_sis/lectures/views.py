from django.shortcuts import render
from .models import Lecture, Course
from django.http import Http404



def course_index(request):
    try:
        course_list = Course.objects.order_by("pk")
    except Course.DoesNotExist:
        course_list = ["No courses found"]
    context = {'course_list':course_list}
    return render(request, 'lectures/course_index.html', context)

def class_index(request, course_id):
    try:    
        course = Course.objects.get(pk=course_id)
        num_courses = len(course.lecture_set.all())
        #Stores each lecture object in a list for access in template
        lecture_list = [course.lecture_set.get(pk=x) for x in range(1, num_courses +1)]
    except Course.DoesnNotExist or Lecture.DoesNotExist:
        lecture_list = ['No classes found.']
    context = {'lecture_list':lecture_list}
    return render(request, 'lectures/class_index.html', context)

def class_detail(request, class_id):
    try:
        lecture = Lecture.objects.get(pk=class_id)
    except Lecture.DoesNotExist:
        raise Http404("This class does not exist")
    return render(request, 'lectures/class_detail.html', {'lecture':lecture})
                                                          


