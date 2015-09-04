from django.conf.urls import patterns, url

from scholarships import views

urlpatterns = patterns('courses.views',
    url(r'^step1-success$', views.ScholarshipApplicationStep1ViewSuccess.as_view(), name="application-1-success"),
    url(r'^step2-success$', views.ScholarshipApplicationStep2ViewSuccess.as_view(), name="application-2-success"),
    url(r'^$', views.ScholarshipApplicationStep1View.as_view(), name="application-1"),
    url(r'^(?P<uuid>[\w.-]+)', views.ScholarshipApplicationStep2View.as_view(), name="application-2"),
)
