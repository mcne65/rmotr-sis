from braces.views import LoginRequiredMixin

from django.views.generic import DetailView
from django.http import Http404

import markdown

from .models import Lecture, CourseInstance


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

    def get_context_data(self, **kwargs):
        context = super(CourseInstanceDetailView, self).get_context_data(**kwargs)

        # if user is staff show all lectures, otherwise show only published ones
        if self.request.user.is_staff:
            context['lectures'] = self.object.lecture_set.all()
        else:
            context['lectures'] = self.object.lecture_set.filter(published=True)

        return context


class LectureDetailView(StudentRequiredMixin, LoginRequiredMixin,
                        DetailView):
    model = Lecture
    template_name = 'courses/lecture_detail.html'

    def validate_user_in_courseinstance(self):
        instance = self.object.course_instance
        if self.request.user not in instance.students.all():
            raise Http404

    def get_context_data(self, **kwargs):
        if not self.object.published and not self.request.user.is_staff:
            # only staff uses can see not published lectures
            raise Http404

        context = super(LectureDetailView, self).get_context_data(**kwargs)
        context['html_content'] = markdown.markdown(self.object.content)

        assignments = self.object.get_assignments_for_user(self.request.user)
        context['assignments'] = assignments

        # if user is staff show the summary of all assignments per student
        if self.request.user.is_staff:
            context['summary'] = self.object.get_assignment_summary()

        return context
