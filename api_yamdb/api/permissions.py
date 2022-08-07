from django.conf import settings
from rest_framework import permissions


class UserRoleIsAllowedRole(permissions.BasePermission):
    """
    Пользователь имеет разрешенную роль.
    В представлении объявите allowed_roles: list = [...].
    Если роль пользователя есть в списке allowed_roles, то возвращается True,
    иначе False.
    """

    message = 'У вас недостаточно прав для этого.'

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return (
                request.user.role in view.allowed_roles
                or request.user.is_superuser
            )
        return False


class UserRoleIsAllowedRoleOrReadOnly(UserRoleIsAllowedRole):
    """
    Запросы для чтения доступны всем.
    Для остальных запросов пользователь должен иметь роль из разрешенных.
    """

    message = 'У вас недостаточно прав для этого.'

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return super().has_permission(request, view)


class UserIsAuthorOrAdmin(permissions.BasePermission):
    """Пользователь - автор объекта или администратор."""

    message = 'Проверьте, являетесь ли вы автором или администратором.'

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return (
                request.user == obj.author
                or request.user.role
                in [settings.MODERATOR_ROLE, settings.ADMIN_ROLE]
                or request.user.is_superuser
            )
        return False
