from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^accounts/', include('accounts.urls')),
    url(r'^courses/', include('courses.urls', namespace="courses")),
    url(r'^assignments/', include('assignments.urls', namespace="assignments")),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('students.urls', namespace="students")),
)
