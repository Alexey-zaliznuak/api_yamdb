from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class Role(models.Model):
    name = models.CharField("Role name", max_length=32)
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


USER_DEAFULT_ROLE = Role.objects.get_or_create(
    **settings.ROLES.get('DEFAULT_USER_ROLE_PERMISSIONS')
)
SUPER_USER_DEAFULT_ROLE = Role.objects.get_or_create(
    **settings.ROLES.get('SUPER_USER_PERMISSIONS')
)


class User(AbstractUser):
    role = models.ForeignKey(
        Role,
        on_delete=models.SET_NULL,
        related_name="Users_with_this_role",
        verbose_name="User Role",
        default=USER_DEAFULT_ROLE[0].pk,
        null=True,
    )

    def clean(self) -> None:
        #superuser can`t lose his role

        if self.is_superuser:
            self.role = SUPER_USER_DEAFULT_ROLE[0]
