from __future__ import division, unicode_literals, absolute_import

from django.views.generic import (CreateView, UpdateView, DeleteView,
                                  ListView, FormView)

from students.models import Person


class PersonListView(ListView):
    model = Person
    template_name = 'students/list.html'
    paginate_by = 50

    def get_queryset(self):
        return Person.objects.all()
