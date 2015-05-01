from django.conf.urls import patterns, url, include

from students import views


urlpatterns = patterns('',
    url('^', include('django.contrib.auth.urls')),
    url(r'^$', views.ProfileListView.as_view()),
)

