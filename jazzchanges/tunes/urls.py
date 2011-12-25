from django.conf.urls.defaults import patterns, include, url

from jazzchanges.tunes import views

urlpatterns = patterns('',
    url(r'^$', views.workspace, name='workspace'),
    url(r'^new/$', views.new_tune, name='new'),
    
    url(r'^(?P<tune_id>\d+)/$', views.view_tune, name='view'),
    url(r'^(?P<tune_id>\d+)/(?P<key>\d+)/$', views.view_tune, name='view_key'),
    url(r'^(?P<tune_id>\d+)/edit/$', views.edit_tune, name='edit'),
    url(r'^(?P<tune_id>\d+)/delete/$', views.delete_tune, name='delete'),
)