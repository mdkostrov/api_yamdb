from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAuthorOrSAFE(BasePermission):
    """Разрешение позволяет вносить изменения в объект только его автору."""
    message = 'Only author can change objects!'

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or obj.author == request.user


class IsAdmin(BasePermission):
    message = 'Only users with admin access can do this'

    def has_permission(self, request, view):
        return request.user.is_superuser or request.user.role == 'admin'


class IsModerator(BasePermission):
    message = 'Only users with moderator access can do this'

    def has_permission(self, request, view):
        return request.user.role == 'moderator'


class IsUser(BasePermission):
    message = 'Only users with user access can do this'

    def has_permission(self, request, view):
        return request.user.role == 'user'
