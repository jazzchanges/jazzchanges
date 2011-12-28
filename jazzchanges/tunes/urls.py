from django.conf.urls.defaults import patterns, include, url

from jazzchanges.tunes import views

urlpatterns = patterns('',
    url(r'^$', views.workspace, name='workspace'),
    url(r'^new/$', views.new_tune, name='new'),
    
    url(r'^(?P<tune_id>\d+)/$', views.view_tune, name='view'),
    url(r'^(?P<tune_id>\d+)/(?P<key>\d+)/$', views.view_tune, name='view_key'),

    url(r'^(?P<tune_id>\d+)/full/$', views.view_tune_fullscreen, name='view_fullscreen'),
    url(r'^(?P<tune_id>\d+)/(?P<key>\d+)/full/$', views.view_tune_fullscreen, name='view_key_fullscreen'),

    url(r'^(?P<tune_id>\d+)/edit/$', views.edit_tune, name='edit'),
    url(r'^(?P<tune_id>\d+)/edit/raw/$', views.edit_tune_raw, name='edit_raw'),
    url(r'^(?P<tune_id>\d+)/edit/meta/$', views.edit_tune_meta, name='edit_meta'),
    url(r'^(?P<tune_id>\d+)/delete/$', views.delete_tune, name='delete'),
)