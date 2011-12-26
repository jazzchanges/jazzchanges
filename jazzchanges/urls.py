from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin

from django.views.generic.simple import direct_to_template

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),

    url(r'^accounts/', include('jazzchanges.customuser.urls')),
    url(r'^accounts/', include('userena.urls')),

    url(r'^tunes/', include('jazzchanges.tunes.urls', namespace='tunes')),
    url(r'^directory/', include('jazzchanges.directory.urls', namespace='directory')),

    url(r'^$', direct_to_template, {'template': 'content/homepage.html'})
)


import settings

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.STATIC_SOURCE}),
    )