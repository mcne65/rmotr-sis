from django.conf.urls import patterns, url

from courses import views

urlpatterns = patterns('courses.views',
    #/courses/
    url(r'^$', views.CourseListView.as_view(), name="course_index"),

    #/courses/<course_id>/
    url(r'^(?P<course_id>[0-9]+)$',
        views.LectureListView.as_view(), name="class_index"),

    #/courses/<course_id>/<class_id>
    url(r'^(?P<course_id>[0-9]+)/(?P<pk>[0-9]+)/$',
        views.LectureDetailView.as_view(), name="lecture_detail"),
)
