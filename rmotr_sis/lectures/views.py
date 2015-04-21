from django.shortcuts import render
from .models import Lecture
from django.http import Http404


def class_index(request):
    try:
        lecture_list = Lecture.objects.order_by('pk')
    except Lecture.DoesNotExist:
        lecture_list = ['No classes found.']
    context = {'lecture_list':lecture_list}
    return render(request, 'lectures/class_index.html', context)

def class_detail(request, class_id):
    try:
        lecture = Lecture.objects.get(pk=class_id)
    except Lecture.DoesNotExist:
        raise Http404("This class does not exist")
    return render(request, 'lectures/class_detail.html', {'lecture':lecture})


