from datetime import datetime

from django.conf import settings
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
        if (not user.is_staff and
                not any([l.course_instance.is_student(user) for l in lectures])):
            raise Http404
        return {'source': self.assignment.source}

    def get_context_data(self, **kwargs):
        context = super(ResolveAssignmentView, self).get_context_data(**kwargs)
        context['next'] = self.request.GET.get('next')

        # # try to find an unfinished attempt for this assignment. If nothing
        # # is found, create a new one.
        # obj, created = AssignmentAttempt.objects.get_or_create(
        #     assignment=self.assignment,
        #     student=self.request.user,
        #     resolved=False,
        #     end_datetime=None,
        #     defaults={'start_datetime': datetime.now()}
        # )
        # if not created:
        #     context['previous_attempt'] = obj
        context['previous_attempts'] = AssignmentAttempt.objects.filter(
            assignment=self.assignment,
            student=self.request.user,
            end_datetime__isnull=False,
        )

        return context

    # def get_success_url(self):
        # next = self.request.GET.get('next')
        # if next:
        #     return next
        # return reverse('student_home')

    @staticmethod
    def build_code_to_execute(source, footer):
        code = """
{source}

import sys
from traceback import *

try:
    {footer}
except AssertionError as e:
    print("{assertion_secret}")
    raise e
except Exception as e:
    etype, value, tb = sys.exc_info()
    print(''.join(format_exception(etype, value, tb)[-2:]))
    raise e
else:
    print("{success_secret}")
        """
        return code.format(**{
            'source': source,
            'footer': footer,
            'assertion_secret': settings.ASSIGNMENTS_ASSERTION_SECRET,
            'success_secret': settings.ASSIGNMENTS_SUCCESS_SECRET
        })

    def form_valid(self, form):

        code = self.build_code_to_execute(
            form.cleaned_data['source'], self.assignment.footer)
        result = run_code(code)

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

        if settings.ASSIGNMENTS_SUCCESS_SECRET in result['output']:
            context['execution'] = {'success': True, 'traceback': None}
            attempt.resolved = True
        elif settings.ASSIGNMENTS_ASSERTION_SECRET in result['output']:
            context['execution'] = {'success': False, 'traceback': None}
        else:
            context['execution'] = {'success': False, 'traceback': result['output']}

        attempt.save()

        return self.render_to_response(context)
