from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAuthor(BasePermission):
    message = 'Only author can change objects!'

    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class IsAdminOrRead(BasePermission):
    def has_permission(self, request, view):
        if (request.user.is_authenticated
                and request.method not in SAFE_METHODS):
            return request.user.is_authenticated and is_admin(request.user)
        return request.method in SAFE_METHODS


class IsAdmin(BasePermission):
    message = 'Only users with admin access can do this'

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and is_admin(request.user))


class IsAdminUpdate(BasePermission):
    message = 'Only users with admin access can do this'

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS
                or is_admin(request.user))


class IsModerator(BasePermission):
    message = 'Only users with moderator access can do this'

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS
                or request.user.role == 'moderator')


def is_admin(user):
    return user.role == 'admin' or user.is_superuser
