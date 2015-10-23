from django import forms

from applications.models import ApplicationReferral, Application
from courses.models import Batch, CourseInstance
from accounts.models import (TIMEZONE_CHOICES, GENDER_CHOICES,
                             OBJECTIVE_CHOICES, OCCUPATION_CHOICES,
                             EXPERIENCE_CHOICES, AVAILABILITY_CHOICES)


class ApplicationFormStep1(forms.ModelForm):

    class Meta:
        model = Application
        fields = ('email', 'first_name', 'last_name')

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            Application.objects.get(email=email, batch=Batch.get_current_batch())
        except Application.DoesNotExist:
            pass
        else:
            raise forms.ValidationError(
                'This email has already applied in this batch')
        return email


class ApplicationModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return '{}, {} {} EST'.format(obj.get_lecture_weekday_display(),  # FIXME: Time in DB is saved as UTC, not EST
                                      obj.start_date.strftime('%B %-dth %Y'),
                                      obj.lecture_utc_time.strftime('%I:%M%p'))


class ApplicationFormStep2(forms.ModelForm):

    gender = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=GENDER_CHOICES
    )
    timezone = forms.ChoiceField(
        widget=forms.Select,
        choices=TIMEZONE_CHOICES
    )
    birth_date = forms.DateField(label="Birth date (MM/DD/YYYY)")
    objective = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=OBJECTIVE_CHOICES,
        label='Which is your primary objective in joining this course?'
    )
    experience = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=EXPERIENCE_CHOICES,
        label='How long have you been learning programming up to this point?'
    )
    availability = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=AVAILABILITY_CHOICES,
        label='How many hours per week can you dedicate to this course?'
    )
    occupation = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=OCCUPATION_CHOICES,
        label='Which is your current occupation?'
    )
    course_instances = ApplicationModelMultipleChoiceField(
        queryset=CourseInstance.objects.filter(batch__accepting_applications=True),
        widget=forms.CheckboxSelectMultiple(),
        label='Select instances that best fit you'
    )
    referrals = forms.ModelMultipleChoiceField(
        queryset=ApplicationReferral.objects.filter(active=True),
        widget=forms.CheckboxSelectMultiple(),
        label='How did you hear about us?'
    )
    referrals_other = forms.CharField(
        label='If you selected "Other" in the previous question, please tell us how',
        max_length=100,
        required=False
    )

    class Meta:
        model = Application
        fields = ('gender', 'timezone', 'birth_date', 'objective', 'experience',
                  'availability', 'occupation', 'course_instances',
                  'referrals', 'referrals_other')

SKILLS_ASSESSMENT = [
    {
        'text': """
What's the correct data type of these values: true, false?
                   """,
        'choices': (
            ('0', 'integer'),
            ('1', 'string'),
            ('2', 'boolean'),
            ('3', 'null'),
        ),
        'correct': '2'
    },
    {
        'text': """
Given the following logic expression:<br/>
<pre>(true or false) and true</pre>
What's the result of the execution?
        """,
        'choices': (
            ('0', 'true'),
            ('1', 'false'),
            ('2', '10'),
            ('3', 'null'),
        ),
        'correct': '0'
    },
    {
        'text': """
If you need to repeat certain action many times as long as a condition is valid, which of the following control structures would you use?
        """,
        'choices': (
            ('0', 'for each loop'),
            ('1', 'case'),
            ('2', 'if'),
            ('3', 'while loop'),
        ),
        'correct': '3'
    },
    {
        'text': """
Which one of the next characteristics is typical of a dictionary (or hash) data structure?
        """,
        'choices': (
            ('0', 'Contains values assigned to a particular and unique key'),
            ('1', 'Contains values in a particular order indexed one after the other'),
            ('2', 'Contains unrepeated values with no order'),
            ('3', 'Contains ordered values that can not be modified after definition time'),
        ),
        'correct': '0'
    },
    {
        'text': """
Why would you use try/except blocks?
        """,
        'choices': (
            ('0', 'To raise an exception in case something went wrong'),
            ('1', 'To analyze the performance and correctness of your code'),
            ('2', 'To catch exceptions and perform the proper action depending on the error type'),
            ('3', 'To perform the same action many times'),
        ),
        'correct': '2'
    },
    {
        'text': """
In "Object Oriented Programming", which one of the following affirmations is true?
        """,
        'choices': (
            ('0', 'You can instantiate many objects from one class'),
            ('1', 'You can instantiate many classes based in one object'),
            ('2', 'Classes and objects are not related at all'),
            ('3', 'Classes and objects are exactly the same thing'),
        ),
        'correct': '0'
    },
    {
        'text': """
Given the following code:<br/>
<pre>
x = 5;
y = x * 2;
y = y * x;
</pre>
Which is the value of "y" after the execution?
        """,
        'choices': (
            ('0', '15'),
            ('1', '50'),
            ('2', '5'),
            ('3', '10'),
        ),
        'correct': '1'
    },
    {
        'text': """
Given the following code:<br/>
<pre>
x = 2;
if (x < 5){
    x = x + 4;
} else if (x == 5){
    x = x * 2;
} else {
    x = x + x - 2;
}
</pre>
Which is the value of "x" after the execution?
        """,
        'choices': (
            ('0', '2'),
            ('1', '4'),
            ('2', '10'),
            ('3', '6'),
        ),
        'correct': '3'
    },
    {
        'text': """
Given the following code:<br/>
<pre>
x = 2;
for (var i=0; i < 10; i++){
    x = x + i;
}
</pre>
Which is the value of "x" after the execution?
        """,
        'choices': (
            ('0', '47'),
            ('1', '2'),
            ('2', '32'),
            ('3', '10'),
        ),
        'correct': '0'
    },
    {
        'text': """
Given the following code:<br/>
<pre>
y = [2, 4, 1]
y[0] = y[0] + y[1]
</pre>
Which is the value of "y" after the execution?
        """,
        'choices': (
            ('0', '[4, 4, 1]'),
            ('1', '[2, 4, 1]'),
            ('2', '[6, 4, 1]'),
            ('3', '[2, 2, 4]'),
        ),
        'correct': '2'
    }
]


class_attrs = {
    'q{}'.format(index): forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=q['choices'],
        label=q['text'])
    for index, q in enumerate(SKILLS_ASSESSMENT)
}
ApplicationFormStep3 = type('ApplicationFormStep3', (forms.Form,), class_attrs)


class ApplicationFormStep4(forms.ModelForm):
    scholarship_q1 = forms.CharField(
        widget=forms.Textarea, max_length=1200,
        label="Please tell us in less than 200 words why you need the scholarship.")
    scholarship_q2 = forms.CharField(
        widget=forms.Textarea, max_length=1200,
        label="Please tell us of that time that you helped someone and it was worth it.")
    scholarship_q3 = forms.CharField(
        widget=forms.Textarea, max_length=1200,
        label="Please tell us what was the most impressive thing you've built by yourself (or with other people).")
    scholarship_q4 = forms.CharField(
        widget=forms.Textarea, max_length=1200,
        label="Please tell us how you've been trying to learn programming by yourself.")
    scholarship_q5 = forms.CharField(
        widget=forms.Textarea, max_length=1200,
        label="Please tell us innovative ways you'd use to hack education and make it more available and affordable to the world.")
    scholarship_q6 = forms.CharField(
        widget=forms.Textarea, max_length=1200,
        label="Will you commit to helping others in order to give back to the community what you've received from this scholarship?")

    class Meta:
        model = Application
        fields = ('scholarship_q1',
                  'scholarship_q2',
                  'scholarship_q3',
                  'scholarship_q4',
                  'scholarship_q5',
                  'scholarship_q6',)


class ApplicationFormStep5(forms.ModelForm):

    scholarship_a1_solution = forms.URLField(
        max_length=1200,
        label='Paste here the gist (https://gist.github.com/) URL with the solution to the assignment')

    def clean_scholarship_a1_solution(self):
        solution = self.cleaned_data['scholarship_a1_solution']
        if 'gist.github.com' not in solution:
            raise forms.ValidationError(
                'Must be a gist.github.com URL')
        return solution

    class Meta:
        model = Application
        fields = ('scholarship_a1_solution',)


class ApplicationFormStep6(forms.ModelForm):

    scholarship_a2_solution = forms.URLField(
        max_length=1200,
        label='Paste here the gist (https://gist.github.com/) URL with the solution to the assignment')

    def clean_scholarship_a2_solution(self):
        solution = self.cleaned_data['scholarship_a2_solution']
        if 'gist.github.com' not in solution:
            raise forms.ValidationError(
                'Must be a gist.github.com URL')
        return solution

    class Meta:
        model = Application
        fields = ('scholarship_a2_solution',)


class ApplicationFormStep7(forms.ModelForm):

    scholarship_a3_solution = forms.URLField(
        max_length=1200,
        label='Paste here the gist (https://gist.github.com/) URL with the solution to the assignment')

    def clean_scholarship_a3_solution(self):
        solution = self.cleaned_data['scholarship_a3_solution']
        if 'gist.github.com' not in solution:
            raise forms.ValidationError(
                'Must be a gist.github.com URL')
        return solution

    class Meta:
        model = Application
        fields = ('scholarship_a3_solution',)
