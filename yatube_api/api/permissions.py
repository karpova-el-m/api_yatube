from rest_framework.permissions import BasePermission, SAFE_METHODS


class PostCommentUserPermission(BasePermission):

    # def has_permission(self, request, view):
    #     if request.method in SAFE_METHODS:
    #         return True
    #     return request.user.is_authenticated()

    # def has_object_permission(self, request, view, obj):
    #     if request.method in ['PUT', 'PATCH', 'DELETE']:
    #         return obj.author == request.user
    #     else:
    #         return True

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.author == request.user
