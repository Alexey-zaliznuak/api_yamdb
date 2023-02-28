from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Roles(models.TextChoices):
        ANONYMOUS = 'anon', _('Anonymous')
        USER = 'user', _('Authenticated user')
        MODERATOR = 'moderator', _('Moderator')
        ADMIN = 'admin', _('Administrator')

    role = models.CharField(
        max_length=16,
        choices=Roles.choices,
        default=Roles.USER,
    )

    def clean(self) -> None:
        # superuser can`t lose his role
        if self.is_superuser:
            self.role = self.Roles.ADMIN
