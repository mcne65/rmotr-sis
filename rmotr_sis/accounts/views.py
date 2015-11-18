from __future__ import division, unicode_literals, absolute_import

from django.views.generic import FormView
from django.http import HttpResponseRedirect
from braces.views import AnonymousRequiredMixin, LoginRequiredMixin

from accounts.forms import UserSignupForm, UpdateProfileForm
from rmotr_sis.utils import send_template_mail


class UpdateProfileView(LoginRequiredMixin, FormView):
    template_name = 'registration/update_profile.html'
    form_class = UpdateProfileForm
    success_url = '/'

    def get_form(self, form_class):
        return form_class(instance=self.request.user,
                          **self.get_form_kwargs())

    def form_valid(self, form):
        if form.is_valid():
            form.save()
        return HttpResponseRedirect(self.get_success_url())


class UserSignupView(AnonymousRequiredMixin, FormView):
    template_name = 'registration/signup.html'
    form_class = UserSignupForm
    success_url = '/accounts/signup-successful'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.set_password(form.cleaned_data['password'])
        user.save()

        # send confirmation email
        subject = 'Thank you for signing up at rmotr.com'
        send_template_mail(subject, 'signup-successful.html',
                           recipient_list=[user.email], context={'user': user})

        return super(UserSignupView, self).form_valid(form)
