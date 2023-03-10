from rest_framework import permissions


ADMIN = 'admin'
MODER = 'moderator'
USER = 'user'


class RolePermission(permissions.BasePermission):
    # contains roles

    # use this for roles with power as staff or admin
    can_edit_all_content = ('admin',)

    # this roles can edit only content what they created
    can_edit_self_content = ('user', 'moderator',)

    def has_permission(self, request, view) -> bool:
        self.can_edit_self_content += self.can_edit_all_content

        return (
            request.method in permissions.SAFE_METHODS
            or (
                request.user.is_authenticated
                and request.user.role in self.can_edit_self_content
            )
        )

    def has_object_permission(self, request, view, obj) -> bool:
        user = request.user

        if (
            request.method in permissions.SAFE_METHODS
            or user.role in self.can_edit_all_content
        ):
            return True

        # author or read only
        if hasattr(obj, 'author'):  # not all models has field author
            if user == obj.author and user.role in self.can_edit_self_content:
                return True

        return False


# content with this perm. can be edit by users with can_edit_all_content roles
class AdminOrReadOnlyRolePermission(RolePermission):
    can_edit_all_content = (ADMIN,)
    can_edit_self_content = ()


# edit content if you are author or moderator/admin
class AuthorOrModeratorCanEditAllRolePermission(RolePermission):
    can_edit_self_content = (USER,)
    can_edit_all_content = (MODER, ADMIN)


class IsAdminUserOrRoleAdmin(permissions.BasePermission):
    def has_permission(self, request, view) -> bool:
        return request.user.has_admin_permissions


# AdminOrReadOnly permissions
CategoriesRolePermission = AdminOrReadOnlyRolePermission
GenresRolePermission = AdminOrReadOnlyRolePermission
TitlesRolePermission = AdminOrReadOnlyRolePermission

# author or 'can_edit_all' permission
ReviewsRolePermission = AuthorOrModeratorCanEditAllRolePermission
CommentsRolePermission = AuthorOrModeratorCanEditAllRolePermission

UserRolePermission = IsAdminUserOrRoleAdmin
