from django.conf.urls import patterns, url

from applications import views


urlpatterns = patterns('applications.views',
    url(r'^$', views.ApplicationStep1View.as_view(), name="application-1"),
    url(r'^step1-success$', views.ApplicationStep1ViewSuccess.as_view(), name="application-1-success"),
    url(r'^(?P<uuid>[\w.-]+)$', views.ApplicationStep2View.as_view(), name="application-2"),
    url(r'^(?P<uuid>[\w.-]+)/skills-assessment$', views.ApplicationStep3View.as_view(), name="application-3"),
    url(r'^(?P<uuid>[\w.-]+)/step3-success$', views.ApplicationStep3ViewSuccess.as_view(), name="application-3-success"),
    url(r'^(?P<uuid>[\w.-]+)/scholarship$', views.ApplicationStep4View.as_view(), name="application-4"),
    url(r'^(?P<uuid>[\w.-]+)/step4-success$', views.ApplicationStep4ViewSuccess.as_view(), name="application-4-success"),
)
