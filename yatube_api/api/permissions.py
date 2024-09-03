from rest_framework.permissions import BasePermission


class PostCommentUserPermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            return obj.author == request.user
        else:
            return True
