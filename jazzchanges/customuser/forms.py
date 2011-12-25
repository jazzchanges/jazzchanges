from django.contrib.auth.forms import PasswordChangeForm

from userena.forms import SignupForm, SignupFormOnlyEmail, AuthenticationForm, ChangeEmailForm, EditProfileForm

from bootstrap.forms import BootstrapForm, Fieldset

from django import forms

# from userena

class NewSignupForm(BootstrapForm, SignupForm):
    class Meta:
        layout = (
            Fieldset('Signup Now', 'username', 'email', 'password1', 'password2'), )

class NewAuthenticationForm(BootstrapForm, AuthenticationForm):
    class Meta:
        layout = (
            Fieldset('Login Now', 'identification', 'password', 'remember_me'), )

class NewChangeEmailForm(ChangeEmailForm, BootstrapForm):
    class Meta:
        layout = (
            Fieldset('Change Email', 'email'), )


# from django itself

class NewPasswordChangeForm(PasswordChangeForm, BootstrapForm):
    class Meta:
        layout = (
            Fieldset('Change Password', 'old_password', 'new_password1', 'new_password2'), )
