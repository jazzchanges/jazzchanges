from django.conf.urls.defaults import patterns, include, url

from jazzchanges.customuser.forms import (  NewSignupForm, NewAuthenticationForm, 
                                            NewChangeEmailForm, NewPasswordChangeForm,
                                            NewSetPasswordForm, NewPasswordResetForm)
from django.contrib.auth import views as auth_views

urlpatterns = patterns('',
    # customize userena forms and stuff
    url(r'^signup/$', 'userena.views.signup', {'signup_form': NewSignupForm}),

    url(r'^signin/$', 'userena.views.signin', {'auth_form': NewAuthenticationForm}),

    url(r'^(?P<username>[\.\w]+)/email/$', 'userena.views.email_change', {'email_form': NewChangeEmailForm}),

    url(r'^(?P<username>[\.\w]+)/password/$', 
        'userena.views.password_change', 
        {'pass_form': NewPasswordChangeForm, 'template_name': 'userena/password_form.html'}),\
    
    url(r'^password/reset/$',
       auth_views.password_reset,
       {'password_reset_form': NewPasswordResetForm,
        'template_name': 'userena/password_reset_form.html',
        'email_template_name': 'userena/emails/password_reset_message.txt'},
       name='userena_password_reset'),

    url(r'^password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
       auth_views.password_reset_confirm,
       {'set_password_form': NewSetPasswordForm,
        'template_name': 'userena/password_reset_confirm_form.html'},
       name='userena_password_reset_confirm'),
)