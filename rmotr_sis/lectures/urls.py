from django.conf.urls import patterns, include, url

from lectures import views

urlpatterns = patterns('lectures.views',
    #/courses/
    url(r'^$', views.CourseListView.as_view(), name="course_index"),
    #/courses/<course_id>/
    url(r'^(?P<course_id>[0-9]+)$', views.class_index, name="class_index"),
    #/courses/<course_id>/<class_id>
    url(r'^(?P<course_id>[0-9]+)/(?P<pk>[0-9]+)/$', views.ClassDetailView.as_view(), name="class_detail"),
)
