from django.conf.urls import patterns, url

from students import views


urlpatterns = patterns('',
    url(r'^$', views.StudentListView.as_view(), name='student_list'),
)
