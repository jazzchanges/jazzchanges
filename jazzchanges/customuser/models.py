from django.db import models

from django.utils.translation import ugettext_lazy as _

from userena.models import UserenaBaseProfile

class UserProfile(UserenaBaseProfile):
    user = models.OneToOneField('auth.User', unique=True, verbose_name=_('user'), related_name='my_profile')