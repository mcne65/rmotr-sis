from datetime import datetime

from django.core.urlresolvers import reverse
from django.contrib import messages
from django.views.generic import FormView
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404

from braces.views import LoginRequiredMixin

from .models import Assignment, AssignmentAttempt
from .forms import ResolveAssignmentForm
from .utils import run_code


class ResolveAssignmentView(LoginRequiredMixin, FormView):
    form_class = ResolveAssignmentForm
    template_name = 'courses/resolve_assignment.html'

    def get_initial(self):
        self.assignment = get_object_or_404(Assignment, pk=self.kwargs['pk'])

        # check if the user has permissions to see this assignment
        user = self.request.user
        lectures = self.assignment.lecture_set.all()
        for lecture in lectures:
            if user.is_staff or lecture.course_instance.is_student(user):
                return {'source': self.assignment.source}
        raise Http404

    def get_context_data(self, **kwargs):
        context = super(ResolveAssignmentView, self).get_context_data(**kwargs)
        context['next'] = self.request.GET.get('next')

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

        return context

    def get_success_url(self):
        next = self.request.GET.get('next')
        if next:
            return next
        return reverse('student_home')

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
