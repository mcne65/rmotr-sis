from django.conf.urls import patterns, url

from courses import views

urlpatterns = patterns('courses.views',
    url(r'^(?P<pk>[0-9]+)$',
        views.CourseInstanceDetailView.as_view(), name="course_detail"),

    url(r'^lectures/(?P<pk>[0-9]+)/$',
        views.LectureDetailView.as_view(), name="lecture_detail"),

    url(r'^assignments/(?P<pk>[0-9]+)/$',
        views.ResolveAssignmentView.as_view(), name="resolve_assignment"),
)
