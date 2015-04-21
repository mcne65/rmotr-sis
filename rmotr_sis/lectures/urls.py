from django.conf.urls import patterns, include, url

from lectures import views

urlpatterns = patterns('lectures.views',
    url(r'^$', views.class_index, name="class_index"), 
    url(r'^(?P<class_id>[0-9]+)$', views.class_detail, name="class_detail"),
)
