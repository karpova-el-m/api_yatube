from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthorOrReadOnly(BasePermission):
    """Разделяет права для автора и авторизованного пользователя."""
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user or request.method in SAFE_METHODS
