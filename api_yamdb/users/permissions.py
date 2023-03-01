from rest_framework import permissions


class RolePermission(permissions.BasePermission):
    # contains roles

    # use this for roles with power as staff or admin
    can_edit_all_content = ('admin',)

    # this roles can edit only content what they created
    can_edit_self_content = ('user',)

    def has_permission(self, request, view) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True

    def has_object_permission(self, request, view, obj) -> bool:
        user = request.user

        if user.role in self.can_edit_all_content:
            return True

        if request.method in permissions.SAFE_METHODS:
            return True

        # author or read only
        if hasattr(obj, 'author'): # not all models has field author
            if user == obj.author and user.role in self.can_edit_self_content:
                return True

            return False
   
        # for models such as Genre, Category: they can edit only by admin/moder
        else:
            return user.role in self.can_edit_all_content


# content with this perm. can be edit by users with can_edit_all_content roles
class AdminOrReadOnlyRolePermission(RolePermission):
    can_edit_all_content = ('admin')


# edit content if you are author or moderator/admin
class AuthorOrCanEditAllRolePermission(RolePermission):
    can_edit_self_content = ('user')
    can_edit_all_content = ('moderator', 'admin')


# AdminOrReadOnly permissions
TitlesRolePermission = AdminOrReadOnlyRolePermission
CategoriesRolePermission = AdminOrReadOnlyRolePermission
GenresRolePermission = AdminOrReadOnlyRolePermission

# author or 'can_edit_all' permission
ReviewsRolePermission = AuthorOrCanEditAllRolePermission
CommentsRolePermission = AuthorOrCanEditAllRolePermission
