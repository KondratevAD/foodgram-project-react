from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """Модель пользователя"""
    class Roles(models.TextChoices):
        ADMIN = 'admin', _('Administrator')
        USER = 'user', _('User')
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(_('email address'), max_length=254, unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    role = models.CharField(
        _('role'), choices=Roles.choices, default=Roles.USER, max_length=30
    )

    @property
    def is_admin(self):
        return self.role == 'admin' or self.is_superuser

    @property
    def is_user(self):
        return self.role == 'user'

    class Meta:
        ordering = ('username',)
