from django import forms

from scholarships.models import ScholarshipApplication


class ScholarshipApplicationFormStep1(forms.ModelForm):

    class Meta:
        model = ScholarshipApplication
        fields = ('email', 'first_name', 'last_name')


class ScholarshipApplicationFormStep2(forms.ModelForm):

    class Meta:
        model = ScholarshipApplication
        fields = ('gender', 'timezone', 'birth_date', 'objective', 'experience',
                  'availability', 'occupation', 'course_instances')
