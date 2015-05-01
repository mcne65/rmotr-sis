from django.conf.urls import patterns, url

from students import views


urlpatterns = patterns('',
    url(r'^$', views.ProfileListView.as_view(), name='list'),
)
