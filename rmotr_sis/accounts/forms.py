from __future__ import division, unicode_literals, absolute_import

from django import forms

from accounts.models import User, TIMEZONE_CHOICES


class UserSignupForm(forms.ModelForm):

    # auth data
    email = forms.EmailField(label='Email address')
    password = forms.CharField(max_length=128, widget=forms.PasswordInput())
    repeat_password = forms.CharField(max_length=128, widget=forms.PasswordInput())

    # personal data
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    timezone = forms.CharField(
        max_length=150, widget=forms.Select(choices=TIMEZONE_CHOICES))
    birth_date = forms.DateField()

    # accounts
    github_handle = forms.CharField(max_length=50)
    cloud9_handle = forms.CharField(max_length=50)


    class Meta:
        model = User
        fields = [
            # auth data
            'username', 'email', 'password', 'repeat_password',

            # personal data
            'first_name', 'last_name', 'timezone', 'birth_date',

            # accounts
            'twitter_handle', 'github_handle', 'cloud9_handle',
        ]

    def clean(self):
        cleaned_data = super(UserSignupForm, self).clean()

        # validate repeated password
        if cleaned_data['password'] != cleaned_data['repeat_password']:
            raise forms.ValidationError('Password is not correctly repeated.')

        return cleaned_data
