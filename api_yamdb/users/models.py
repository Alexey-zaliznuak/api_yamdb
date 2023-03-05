from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError


class User(AbstractUser):
    class Roles(models.TextChoices):
        USER = 'user', _('Authenticated user')
        MODERATOR = 'moderator', _('Moderator')
        ADMIN = 'admin', _('Administrator')

    email = models.EmailField(_('email address'), max_length=254, unique=True)
    bio = models.TextField("biography", max_length=500, null=True)
    role = models.CharField(
        "user role",
        max_length=16,
        choices=Roles.choices,
        default=Roles.USER,
    )
    confirm_code = models.CharField(editable=False, max_length=64)

    def clean(self) -> None:
        # superuser can`t lose his role
        if self.is_staff or self.is_superuser:
            self.role = self.Roles.ADMIN

        if self.username == 'me':
            raise ValidationError('uncorrect username')

    def __str__(self) -> str:
        return self.email + " " + self.username
