from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Participant(AbstractUser):
    class Meta:
        db_table = 'participant'

    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        _('Username'),
        max_length=50,
        unique=True,
        help_text=_('Required. Used for log in paired with a password. 50 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={'unique': _('A participant with that username already exists.'), },
    )
    name = models.CharField(
        _('Name'),
        max_length=50,
        unique=True,
        help_text=_('Required. Used for signing opinions. 50 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={'unique': _('Another participant signs opinions with this name.'), },
    )
    email = models.EmailField(
        _('Email address'),
        blank=False,
        help_text=_('Required. Used for password recovery.'),
    )

    time_zone = models.CharField(_('Time zone'), max_length=50, default='UTC')
    l1 = models.CharField(_('Primary language'), max_length=20, choices=settings.LANGUAGES, default='en')
    l2 = models.CharField(_('Secondary language'), max_length=20, choices=settings.LANGUAGES, blank=True)
    about = models.TextField(_('About'), default='', blank=True)
