from django.conf.urls import patterns, url

from applications import views

urlpatterns = patterns('applications.views',
    url(r'^step1-success$', views.ApplicationStep1ViewSuccess.as_view(), name="application-1-success"),
    url(r'^step2-success$', views.ApplicationStep2ViewSuccess.as_view(), name="application-2-success"),
    url(r'^step3-success$', views.ApplicationStep3ViewSuccess.as_view(), name="application-3-success"),
    url(r'^$', views.ApplicationStep1View.as_view(), name="application-1"),
    url(r'^(?P<uuid>[\w.-]+)$', views.ApplicationStep2View.as_view(), name="application-2"),
    url(r'^(?P<uuid>[\w.-]+)/skills-assessment', views.ApplicationStep3View.as_view(), name="application-3"),
)
