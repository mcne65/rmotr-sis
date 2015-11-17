from django.conf.urls import patterns, url, include
from django.views.generic import TemplateView

from accounts.views import UserSignupView

urlpatterns = patterns('',
    url('^', include('django.contrib.auth.urls')),

    # Sign up
    url(r'signup/$', UserSignupView.as_view(), name='user_signup'),
    url(r'signup-successful/$',
        TemplateView.as_view(template_name="registration/signup-successful.html")),
)
