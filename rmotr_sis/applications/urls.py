from django.conf import settings
from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from applications import views


urlpatterns = patterns(
    'applications.views',
    url(r'^$', views.ApplicationStep1View.as_view(), name="application-1"),

    url(r'^(?P<uuid>[\w.-]+)$', views.ApplicationStep2View.as_view(), name="application-2"),

    url(r'^(?P<uuid>[\w.-]+)/skills-assessment$', views.ApplicationStep3View.as_view(), name="application-3"),

    url(r'^(?P<uuid>[\w.-]+)/scholarship$', views.ApplicationStep4View.as_view(), name="application-4"),

    # scholarship assignments
    url(r'^(?P<uuid>[\w.-]+)/scholarship/assignments/1$', views.ApplicationStep5View.as_view(), name="application-5"),
    url(r'^(?P<uuid>[\w.-]+)/scholarship/assignments/2$', views.ApplicationStep6View.as_view(), name="application-6"),
    url(r'^(?P<uuid>[\w.-]+)/scholarship/assignments/3$', views.ApplicationStep7View.as_view(), name="application-7"),

    # stripe checkout
    url(r'^(?P<uuid>[\w.-]+)/checkout$', views.ApplicationCheckoutView.as_view(), name="application-checkout"),
)

if settings.DEBUG:
    urlpatterns += patterns(
        'applications.views',
        url(
            r'^conirmation-step-template/(?P<step>[0-9]+)$',
            views.ConfirmationStepView.as_view(), name="confirmation-template"),
    )
