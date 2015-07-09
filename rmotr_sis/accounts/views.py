from __future__ import division, unicode_literals, absolute_import

from django.views.generic import FormView
from braces.views import AnonymousRequiredMixin

from accounts.forms import UserSignupForm
from rmotr_sis.utils import send_template_mail


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
        from_email = 'no-reply@rmotr.com'
        send_template_mail(subject, 'signup-successful.html',
                           from_email=from_email, recipient_list=[user.email])

        return super(UserSignupView, self).form_valid(form)
