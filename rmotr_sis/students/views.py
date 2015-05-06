from __future__ import division, unicode_literals, absolute_import

from braces.views import StaffuserRequiredMixin, LoginRequiredMixin

from django.db.models import Q
from django.views.generic import ListView, TemplateView

from students.models import Profile
from courses.models import CourseInstance


class ProfileListView(StaffuserRequiredMixin, ListView):
    model = Profile
    template_name = 'students/list.html'
    paginate_by = 50

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Profile.objects.filter(
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query) |
                Q(lg_full_name__icontains=query) |
                Q(email__icontains=query)
            )
        else:
            return Profile.objects.all()


class StudentHomeView(LoginRequiredMixin, TemplateView):
    template_name = 'students/home.html'

    def get_context_data(self, **kwargs):
        if self.request.user.is_staff:
            courses = CourseInstance.objects.all()
        else:
            courses = self.request.user.profile.courseinstance_set.all()
        context = {
            'courses': courses
        }
        return context
