from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin

from django.views.generic.simple import direct_to_template

from jazzchanges.customuser.forms import (  NewSignupForm, NewAuthenticationForm, 
                                            NewChangeEmailForm, NewPasswordChangeForm)

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),

    # customize userena forms and stuff
    url(r'^accounts/signup/$', 'userena.views.signup', {'signup_form': NewSignupForm}),
    url(r'^accounts/signin/$', 'userena.views.signin', {'auth_form': NewAuthenticationForm}),

    url(r'^accounts/(?P<username>[\.\w]+)/email/$', 'userena.views.email_change', {'email_form': NewChangeEmailForm}),
    url(r'^accounts/(?P<username>[\.\w]+)/password/$', 
        'userena.views.password_change', 
        {'pass_form': NewPasswordChangeForm, 'template_name': 'userena/password_form.html'}),

    url(r'^accounts/', include('userena.urls')),
    url(r'^tunes/', include('jazzchanges.tunes.urls', namespace='tunes')),

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