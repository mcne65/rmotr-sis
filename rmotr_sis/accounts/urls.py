from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from accounts.views import UserSignupView

urlpatterns = patterns('',
    url(r'login/$', 'django.contrib.auth.views.login'),
    url(r'logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),

    url(r'signup/$', UserSignupView.as_view(), name='user_signup'),
    url(r'^signup-successful/', TemplateView.as_view(
        template_name="registration/signup-successful.html")),
)
