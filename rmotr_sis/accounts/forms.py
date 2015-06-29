from __future__ import division, unicode_literals, absolute_import

from django import forms

from accounts.models import User, TIMEZONE_CHOICES


class UserSignupForm(forms.ModelForm):

    email = forms.EmailField(label='Email address')
    password = forms.CharField(max_length=128)
    repeat_password = forms.CharField(max_length=128)

    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)

    birth_date = forms.DateField()
    github_handle = forms.CharField(max_length=50)
    cloud9_handle = forms.CharField(max_length=50)
    timezone = forms.CharField(
        max_length=150, widget=forms.Select(choices=TIMEZONE_CHOICES))


    class Meta:
        model = User
        fields = [
            # auth data
            'username',
            'email',
            'password',
            'repeat_password',

            # personal data
            'first_name',
            'last_name',
            'timezone',
            'birth_date',

            # accounts
            'twitter_handle',
            'github_handle',
            'cloud9_handle',
        ]
