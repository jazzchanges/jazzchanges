from django.conf.urls.defaults import patterns, include, url

from jazzchanges.directory import views

urlpatterns = patterns('',
    url(r'^$', views.root, name='root'),
    
    url(r'^(?P<tune_id>\d+)/$', views.view_tune, name='view'),
    url(r'^(?P<tune_id>\d+)/(?P<key>\d+)/$', views.view_tune, name='view_key'),

    url(r'^(?P<tune_id>\d+)/full/$', views.view_tune_fullscreen, name='view_fullscreen'),
    url(r'^(?P<tune_id>\d+)/(?P<key>\d+)/full/$', views.view_tune_fullscreen, name='view_key_fullscreen'),
)