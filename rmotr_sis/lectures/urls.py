from django.conf.urls import patterns, include, url

from lectures import views

urlpatterns = patterns('',
    url(r'^$', views.class_index, name="class_index"), 
)
