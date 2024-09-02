from rest_framework import viewsets
from posts.models import Post, Group, Comment
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import BasePermission, IsAdminUser, IsAuthenticated

from .serializers import PostSerializer, CommentSerializer, GroupSerializer


class GroupUserPermission(BasePermission):

    def has_permission(self, request, view):
        if request.method in ['PUT', 'PATCH', 'POST', 'DELETE']:
            return request.user.is_staff
            # return status.HTTP_405_METHOD_NOT_ALLOWED
        else:
            return True


class PostCommentUserPermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            return obj.author == request.user
        else:
            return True


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (PostCommentUserPermission, IsAuthenticated, )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (PostCommentUserPermission, IsAuthenticated)

    def get_queryset(self):
        pk = self.kwargs['post_pk']
        queryset = Comment.objects.filter(post=pk)
        return queryset

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            post_id=self.kwargs.get('post_pk')
        )


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (GroupUserPermission, IsAuthenticated)
    # permission_classes = (IsAdminUser, )
