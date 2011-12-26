from django.conf.urls.defaults import patterns, include, url

from jazzchanges.directory import views

urlpatterns = patterns('',
    url(r'^$', views.root, name='root'),
    url(r'^search/$', views.search, name='search'),
    
    url(r'^(?P<tune_id>\d+)/(?P<artist_slug>[-\w]+)/(?P<title_slug>[-\w]+)/$', views.view_tune, name='view'),
    url(r'^(?P<tune_id>\d+)/(?P<artist_slug>[-\w]+)/(?P<title_slug>[-\w]+)/(?P<key>\d+)/$', views.view_tune, name='view_key'),

    url(r'^(?P<tune_id>\d+)/(?P<artist_slug>[-\w]+)/(?P<title_slug>[-\w]+)/full/$', views.view_tune_fullscreen, name='view_fullscreen'),
    url(r'^(?P<tune_id>\d+)/(?P<artist_slug>[-\w]+)/(?P<title_slug>[-\w]+)/(?P<key>\d+)/full/$', views.view_tune_fullscreen, name='view_key_fullscreen'),
)