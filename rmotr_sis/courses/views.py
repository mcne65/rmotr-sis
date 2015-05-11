from __future__ import division, unicode_literals, absolute_import

from datetime import datetime

from braces.views import LoginRequiredMixin

from django.core.urlresolvers import reverse
from django.contrib import messages
from django.views.generic import DetailView, FormView
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404

from .models import Lecture, CourseInstance, Assignment, AssignmentAttempt
from .forms import ResolveAssignmentForm
from .utils import run_code


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
        if self.request.user not in self.object.students.all():
            raise Http404


class LectureDetailView(StudentRequiredMixin, LoginRequiredMixin,
                        DetailView):
    model = Lecture
    template_name = 'courses/lecture_detail.html'

    def validate_user_in_courseinstance(self):
        instance = self.object.course_instance
        if self.request.user not in instance.students.all():
            raise Http404

    def get_context_data(self, **kwargs):
        context = super(LectureDetailView, self).get_context_data(**kwargs)

        assignments = self.object.assignment_set.all()
        for a in assignments:
            a.resolved = a.is_resolved_by_student(self.request.user)
        context['assignments'] = assignments

        # if user is staff show the summary of all assignments per student
        if self.request.user.is_staff:
            all_assignments = {}
            for student in self.object.course_instance.students.all():
                all_assignments.setdefault(student, {})
                for a in assignments:
                    all_assignments[student][a] = a.is_resolved_by_student(student)
            context['all_assignments'] = all_assignments

        return context


class ResolveAssignmentView(LoginRequiredMixin, FormView):
    form_class = ResolveAssignmentForm
    template_name = 'courses/resolve_assignment.html'

    def get_initial(self):
        self.assignment = get_object_or_404(Assignment, pk=self.kwargs['pk'])
        allowed_students = self.assignment.lecture.course_instance.students.all()
        if not self.request.user.is_staff and self.request.user not in allowed_students:
            raise Http404
        return {'source': self.assignment.source}

    def get_context_data(self, **kwargs):
        context = super(ResolveAssignmentView, self).get_context_data(**kwargs)

        # try to find an unfinished attempt for this assignment. If nothing
        # is found, create a new one.
        obj, created = AssignmentAttempt.objects.get_or_create(
            assignment=self.assignment,
            student=self.request.user,
            resolved=False,
            end_datetime=None,
            defaults={'start_datetime': datetime.now()}
        )
        if not created:
            context['previous_attempt'] = obj
        context['lecture'] = self.assignment.lecture

        return context

    def get_success_url(self):
        return reverse('courses:lecture_detail',
                       kwargs={'pk': self.assignment.lecture.id})

    def form_valid(self, form):

        code = '{}\n\n{}'.format(form.cleaned_data['source'],
                                 self.assignment.footer)
        result = run_code(code)

        # finish the attempt and check if it's a valid solution or not
        attempt = AssignmentAttempt.objects.get(
            assignment=self.assignment, student=self.request.user,
            end_datetime=None, resolved=False)
        attempt.source = result['code']
        attempt.output = result['output']
        attempt.errors = result.get('errors')
        if result.get('time'):
            attempt.execution_time = float(result['time'].rstrip('\n'))
        if not attempt.errors and not attempt.output:
            # no assert failed, the solution is correct
            attempt.resolved = True
            messages.success(
                self.request, 'Excelent! You have resolved the assignment.')
        else:
            messages.error(
                self.request,
                'Ouch! The solution you posted was incorrect, please try again.')
        attempt.end_datetime = datetime.now()
        attempt.save()

        return HttpResponseRedirect(self.get_success_url())
