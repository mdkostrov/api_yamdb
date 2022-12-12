from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAuthorOrSAFE(BasePermission):
    """Разрешение позволяет вносить изменения в объект только его автору."""
    message = 'Only author can change objects!'

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or obj.author == request.user
