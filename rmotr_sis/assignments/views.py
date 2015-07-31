from datetime import datetime

from django.views.generic import FormView
from django.http import Http404
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
        if (not user.is_staff and
                not any([l.course_instance.is_student(user) for l in lectures])):
            raise Http404
        return {'source': self.assignment.source}

    def get_context_data(self, **kwargs):
        context = super(ResolveAssignmentView, self).get_context_data(**kwargs)
        context['next'] = self.request.GET.get('next')
        context['assignment'] = self.assignment

        context['previous_attempts'] = AssignmentAttempt.objects.filter(
            assignment=self.assignment,
            student=self.request.user,
            end_datetime__isnull=False,
        )

        return context

    @staticmethod
    def build_code_to_execute(source, footer):
        code = """
{student_source}

import sys
import unittest

{our_tests}

suite = unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__])
result = suite.run(unittest.TestResult())

if not result.wasSuccessful():
  unittest.TextTestRunner(stream=sys.stderr, verbosity=2).run(suite)
        """
        return code.format(**{'student_source': source, 'our_tests': footer})

    def form_valid(self, form):

        code = self.build_code_to_execute(
            form.cleaned_data['source'], self.assignment.footer)
        result = run_code(code)

        # register a new attempt for this assignemnt
        attempt = AssignmentAttempt(
            assignment=self.assignment,
            student=self.request.user,
            student_source=form.cleaned_data['source'],
            start_datetime=datetime.now(),
            end_datetime=datetime.now()
        )

        # execution details
        attempt.source = result['code']
        attempt.output = result['output']
        attempt.errors = result.get('errors')
        if result.get('time'):
            attempt.execution_time = float(result['time'].rstrip('\n'))

        context = self.get_context_data(form=form)
        context['execution'] = {'success': True, 'traceback': None}
        if result.get('errors'):
            # tests execution failed, send traceback to the template
            context['execution'] = {'success': False, 'traceback': result['errors']}
        else:
            # mark the assignment as resolved
            attempt.resolved = True

        attempt.save()

        return self.render_to_response(context)
