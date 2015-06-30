from __future__ import division, unicode_literals, absolute_import

from django.views.generic import FormView

from accounts.forms import UserSignupForm


class UserSignupView(FormView):
    template_name = 'registration/signup.html'
    form_class = UserSignupForm
    success_url = '/accounts/signup-successful'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.set_password(form.cleaned_data['password'])
        user.save()

        # TODO: Send confirmation email

        return super(UserSignupView, self).form_valid(form)
