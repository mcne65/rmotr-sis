from __future__ import division, unicode_literals, absolute_import

from django import forms

from .models import Assignment


class ResolveAssignmentForm(forms.ModelForm):

    class Meta:
        model = Assignment
        fields = ['source']
