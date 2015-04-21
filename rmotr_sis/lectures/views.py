from django.shortcuts import render
from .models import Lecture


def class_index(request):
    try:
        lecture_list = Lecture.objects.order_by('pk')
    except Lecture.DoesNotExist:
        lecture_list = ['No classes found.']
    context = {'lecture_list':lecture_list}
    return render(request, 'lectures/class_index.html', context)


