from django.conf.urls import patterns, include, url

from students import views


urlpatterns = patterns('',
    url(r'^$', views.persons_list),
)
