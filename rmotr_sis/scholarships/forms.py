from django import forms

from scholarships.models import ScholarshipApplication
from courses.models import CourseInstance
from accounts.models import (TIMEZONE_CHOICES, GENDER_CHOICES,
                             OBJECTIVE_CHOICES, OCCUPATION_CHOICES,
                             EXPERIENCE_CHOICES, AVAILABILITY_CHOICES)


class ScholarshipApplicationFormStep1(forms.ModelForm):

    class Meta:
        model = ScholarshipApplication
        fields = ('email', 'first_name', 'last_name')


class ScholarshipModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return '{}, {} UTC'.format(obj.get_lecture_weekday_display(),
                                   obj.start_date.strftime('%B %-dth %Y %I:%M%p'))


class ScholarshipApplicationFormStep2(forms.ModelForm):

    gender = forms.CharField(
        max_length=15, widget=forms.RadioSelect(choices=GENDER_CHOICES))
    timezone = forms.CharField(
        max_length=150, widget=forms.Select(choices=TIMEZONE_CHOICES))
    birth_date = forms.DateField(label="Birth date (MM/DD/YYYY)")
    objective = forms.CharField(
            max_length=150, widget=forms.RadioSelect(choices=OBJECTIVE_CHOICES),
            label='Which is your primary objective in joining this course?')
    experience = forms.CharField(
            max_length=150, widget=forms.RadioSelect(choices=EXPERIENCE_CHOICES),
            label='How many hours have you spent learning programming up to this point?')
    availability = forms.CharField(
            max_length=150, widget=forms.RadioSelect(choices=AVAILABILITY_CHOICES),
            label='How many hours per week can you dedicate to this course?')
    occupation = forms.CharField(
            max_length=150, widget=forms.RadioSelect(choices=OCCUPATION_CHOICES),
            label='Which is your current occupation?')
    course_instances = ScholarshipModelMultipleChoiceField(
            queryset=CourseInstance.objects.filter(batch__accepting_applications=True),
            widget=forms.CheckboxSelectMultiple(),
            label='Select instances that best fit you')

    class Meta:
        model = ScholarshipApplication
        fields = ('gender', 'timezone', 'birth_date', 'objective', 'experience',
                  'availability', 'occupation', 'course_instances')

SKILLS_ASSESSMENT = [
    {
        'text': 'Say that f(x) = x + 2. What would be the result of f(5)?',
        'choices': (
            ('0', '5'),
            ('1', '0'),
            ('2', '7'),
            ('3', '2'),
        ),
        'correct': '2'
    },
    {
        'text': 'Say that f(x) = x + 3. What would be the result of f(2)*f(5)?',
        'choices': (
            ('0', '5'),
            ('1', '8'),
            ('2', '40'),
            ('3', '13'),
        ),
        'correct': '2'
    }
]


class_attrs = {
    'q{}'.format(index): forms.CharField(
        max_length=1, label=q['text'],
        widget=forms.RadioSelect(choices=q['choices']))
    for index, q in enumerate(SKILLS_ASSESSMENT)
}
ScholarshipApplicationFormStep3 = type('ScholarshipApplicationFormStep3',
                                       (forms.Form,),
                                       class_attrs)
