from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class Role(models.Model):
    name = models.CharField("Role name", max_length=32, primary_key=True, db_index=True)
    can_read = models.BooleanField(
        "User with this role can read",
        default=False
    )
    can_post_content = models.BooleanField(
        "User with this role can post content",
        default=False
    )
    can_edit_self_content = models.BooleanField(
        "User with this role can edit self content",
        default=False
    )
    can_edit_all_content = models.BooleanField(
        "User with this role can edit all content",
        default=False
    )

    def clean(self):
        if self.can_edit_all_content:
            self.can_edit_self_content = True

    def __str__(self) -> str:
        return self.name


def get_user_default_role():
    return Role.objects.get_or_create(
        **settings.ROLES.get('DEFAULT_USER_ROLE_PERMISSIONS')
    )[0].pk

def get_super_user_default_role():
    return Role.objects.get_or_create(
        **settings.ROLES.get('SUPER_USER_ROLE_PERMISSIONS')
    )[0]


class User(AbstractUser):
    role = models.ForeignKey(
        Role,
        on_delete=models.SET_DEFAULT,
        related_name="Users_with_this_role",
        verbose_name="User Role",
        to_field='name',
        default=get_user_default_role,
    )

    def clean(self) -> None:
        # superuser can`t lose his role

        if self.is_superuser:
            self.role = get_super_user_default_role()
