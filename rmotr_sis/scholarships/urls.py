from django.conf.urls import patterns, url

from scholarships import views

urlpatterns = patterns('courses.views',
    url(r'^step1-success$', views.ScholarshipApplicationStep1ViewSuccess.as_view(), name="application-1-success"),
    url(r'^step2-success$', views.ScholarshipApplicationStep2ViewSuccess.as_view(), name="application-2-success"),
    url(r'^step3-success$', views.ScholarshipApplicationStep3ViewSuccess.as_view(), name="application-3-success"),
    url(r'^$', views.ScholarshipApplicationStep1View.as_view(), name="application-1"),
    url(r'^(?P<uuid>[\w.-]+)$', views.ScholarshipApplicationStep2View.as_view(), name="application-2"),
    url(r'^(?P<uuid>[\w.-]+)/skills-assessment', views.ScholarshipApplicationStep3View.as_view(), name="application-3"),
)
