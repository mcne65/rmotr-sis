from __future__ import division, unicode_literals, absolute_import

from django import forms

from accounts.models import (User, TIMEZONE_CHOICES, GENDER_CHOICES,
                             OBJECTIVE_CHOICES, OCCUPATION_CHOICES)


class UserSignupForm(forms.ModelForm):

    # auth data
    email = forms.EmailField(label='Google account email',
                             help_text=('We require Google account emails to '
                                        'use them in our Hangout sessions.'))
    password = forms.CharField(max_length=128, widget=forms.PasswordInput())
    repeat_password = forms.CharField(max_length=128, widget=forms.PasswordInput())

    # personal data
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    gender = forms.CharField(
        max_length=15, widget=forms.Select(choices=GENDER_CHOICES))
    timezone = forms.CharField(
        max_length=150, widget=forms.Select(choices=TIMEZONE_CHOICES))
    birth_date = forms.DateField(label="Birth date (MM/DD/YYYY)")

    # accounts
    github_handle = forms.CharField(max_length=50, label='Github username')
    cloud9_handle = forms.CharField(max_length=50, label='Cloud9 username')
    twitter_handle = forms.CharField(max_length=50, label='Twitter username',
                                     required=False)
    linkedin_profile_url = forms.URLField(label='URL to your LinkedIn profile',
                                          required=False)

    # extra info
    objective = forms.CharField(
            max_length=150, widget=forms.Select(choices=OBJECTIVE_CHOICES),
            label='Which is your primary objective in joining this course?')
    occupation = forms.CharField(
            max_length=150, widget=forms.Select(choices=OCCUPATION_CHOICES),
            label='Are you currently')

    class Meta:
        model = User
        fields = [
            # auth data
            'username', 'email', 'password', 'repeat_password',

            # personal data
            'first_name', 'last_name', 'gender', 'timezone', 'birth_date',

            # accounts
            'github_handle', 'cloud9_handle', 'twitter_handle',
            'linkedin_profile_url',

            # extra info
            'objective', 'occupation',
        ]

    def clean_email(self):
        email = self.cleaned_data['email']

        # must be unique
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        else:
            raise forms.ValidationError(
                'A user with that email address already exists.')

    def clean(self):
        super(UserSignupForm, self).clean()

        # validate repeated password
        password = self.cleaned_data.get('password')
        repeat_password = self.cleaned_data.get('repeat_password')
        if password and repeat_password and password != repeat_password:
            raise forms.ValidationError('Password is not correctly repeated.')

        return self.cleaned_data
