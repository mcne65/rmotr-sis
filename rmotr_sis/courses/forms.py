from __future__ import division, unicode_literals, absolute_import

from django import forms

from .models import Assignment


class ResolveAssignmentForm(forms.ModelForm):

    class Meta:
        model = Assignment
        fields = ['source']

    def is_valid(self):
        source = self.data['source']
        # request code execution service here

        super(ResolveAssignmentForm, self).is_valid()
