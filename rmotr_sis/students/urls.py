from django.conf.urls import patterns, include, url

from students import views


urlpatterns = patterns('',
    url(r'^$', views.PersonListView.as_view()),
)
