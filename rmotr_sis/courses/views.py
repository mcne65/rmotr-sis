from __future__ import division, unicode_literals, absolute_import

from braces.views import LoginRequiredMixin

from django.views.generic import DetailView, FormView
from django.http import Http404
from django.shortcuts import get_object_or_404

from .models import Lecture, CourseInstance, Assignment
from .forms import ResolveAssignmentForm


class StudentRequiredMixin(object):
    """Allows access to the view only to current students of the course instance

       Staff users can still access to all views despite not participating
       in the course instance.

       NOTE: Each class inheriting from this one must implement the
             `validate_user_in_courseinstance` method.
    """

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not self.request.user.is_staff:
            self.validate_user_in_courseinstance()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class CourseInstanceDetailView(StudentRequiredMixin, LoginRequiredMixin,
                               DetailView):
    model = CourseInstance
    template_name = 'courses/course_detail.html'

    def validate_user_in_courseinstance(self):
        if self.request.user.profile not in self.object.students.all():
            raise Http404


class LectureDetailView(StudentRequiredMixin, LoginRequiredMixin,
                        DetailView):
    model = Lecture
    template_name = 'courses/lecture_detail.html'

    def validate_user_in_courseinstance(self):
        instance = self.object.course_instance
        if self.request.user.profile not in instance.students.all():
            raise Http404


class ResolveAssignmentView(LoginRequiredMixin, FormView):
    form_class = ResolveAssignmentForm
    template_name = 'courses/resolve_assignment.html'

    def get_initial(self):
        assignment = get_object_or_404(Assignment, pk=self.kwargs['pk'])
        return {'source': assignment.source}
