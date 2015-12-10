from django.conf.urls import patterns, include, url
from django.contrib import admin

from students import views


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^courses/', include('courses.urls', namespace="courses")),
    url(r'^assignments/', include('assignments.urls', namespace="assignments")),
    url(r'^students/', include('students.urls', namespace="students")),
    url(r'^applications/', include('applications.urls', namespace="applications")),
    url(r'^social/', include('social.apps.django_app.urls', namespace='social')),
    url(r'^$', views.StudentHomeView.as_view(), name='student_home'),
)
