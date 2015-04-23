from django.conf.urls import patterns, include, url

from lectures import views

urlpatterns = patterns('lectures.views',
    #/courses/
    url(r'^$', views.course_index, name="course_index"),
    #/courses/<course_id>/
    url(r'^(?P<course_id>[0-9]+)$', views.class_index, name="class_index"),
    #/courses/<course_id>/<class_id>
    url(r'^(?P<course_id>[0-9]+)/(?P<class_id>[0-9]+)/$', views.class_detail, name="class_detail"),
)
