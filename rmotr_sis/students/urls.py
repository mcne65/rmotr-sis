from django.conf.urls import patterns, url

from students import views


urlpatterns = patterns('',
    url(r'students$', views.ProfileListView.as_view(), name='student_list'),
    url(r'$', views.StudentHomeView.as_view(), name='student_home'),
)
