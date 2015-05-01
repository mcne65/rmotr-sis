from __future__ import division, unicode_literals, absolute_import

from braces.views import LoginRequiredMixin

from django.db.models import Q
from django.views.generic import ListView

from students.models import Profile


class ProfileListView(LoginRequiredMixin, ListView):
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
