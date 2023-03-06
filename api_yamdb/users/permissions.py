from rest_framework import permissions


class RolePermission(permissions.BasePermission):
    # contains roles

    # use this for roles with power as staff or admin
    can_edit_all_content = ('admin',)

    # this roles can edit only content what they created
    can_edit_self_content = ('user', 'moderator',)

    def has_permission(self, request, view) -> bool:
        self.can_edit_self_content += self.can_edit_all_content

        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.is_anonymous:
            return False

        return request.user.role in self.can_edit_self_content

    def has_object_permission(self, request, view, obj) -> bool:
        user = request.user

        if request.method in permissions.SAFE_METHODS:
            return True

        if user.role in self.can_edit_all_content:
            return True

        # author or read only
        if hasattr(obj, 'author'):  # not all models has field author
            if user == obj.author and user.role in self.can_edit_self_content:
                return True

        return False


# content with this perm. can be edit by users with can_edit_all_content roles
class AdminOrReadOnlyRolePermission(RolePermission):
    can_edit_all_content = ('admin',)


# edit content if you are author or moderator/admin
class AuthorOrModeratorCanEditAllRolePermission(RolePermission):
    can_edit_self_content = ('user',)
    can_edit_all_content = ('moderator', 'admin')


class OnlyRolePermission():
    roles = ('Admin',)

    def has_permission(self, request, view) -> bool:
        if request.user.role in self.roles:
            return True

        return False


class IsAdminUserOrRoleAdmin(permissions.BasePermission):
    def has_permission(self, request, view) -> bool:
        user = request.user

        if user.is_staff or user.is_superuser or user.role == 'admin':
            return True
        return False


class ermtest(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
                request.method in permissions.SAFE_METHODS or
                (request.user.is_authenticated and request.user.role == 'admin')
        )


class ErmTitle(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
                request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
                request.method in permissions.SAFE_METHODS
                or request.user.role == 'admin'
                or request.user.role == 'moderator'
                or obj.author == request.user
        )


# AdminOrReadOnly permissions
CategoriesRolePermission = AdminOrReadOnlyRolePermission
GenresRolePermission = AdminOrReadOnlyRolePermission

# author or 'can_edit_all' permission
TitlesRolePermission = AuthorOrModeratorCanEditAllRolePermission
ReviewsRolePermission = AuthorOrModeratorCanEditAllRolePermission
CommentsRolePermission = AuthorOrModeratorCanEditAllRolePermission

UserRolePermission = IsAdminUserOrRoleAdmin
