from django.conf.urls import patterns, url

from assignments import views

urlpatterns = patterns('courses.views',
    url(r'^(?P<pk>[0-9]+)$',
        views.ResolveAssignmentView.as_view(), name="resolve_assignment"),
)
