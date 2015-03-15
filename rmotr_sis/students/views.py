from __future__ import division, unicode_literals, absolute_import

from django.db.models import Q
from django.views.generic import (CreateView, UpdateView, DeleteView,
                                  ListView, FormView)

from students.models import Person


class PersonListView(ListView):
    model = Person
    template_name = 'students/list.html'
    paginate_by = 50

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Person.objects.filter(
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query) |
                Q(lg_full_name__icontains=query) |
                Q(email__icontains=query)
            )
        else:
            return Person.objects.all()
