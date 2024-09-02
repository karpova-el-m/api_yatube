from django.shortcuts import render
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
        else:
            return True


class PostUserPermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            return obj.author == request.user
        else:
            return True


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (PostUserPermission, IsAuthenticated, )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    # @action(detail=True, methods=['putch', 'put', 'delete'])
    # def get_permissions(request, post_pk=None):
    #     post = get_object_or_404(Post, pk=post_pk)
    #     author = post.author
    #     serializer = PostSerializer(data=request.data)
    #     if request.user == author:
    #         if serializer.is_valid():
    #             serializer.save(data=request.data, partial=True)
    #             return Response(
    #                 serializer.data,
    #                 status=status.HTTP_200_OK
    #             )
    #     else:
    #         return Response(
    #             serializer.errors,
    #             status=status.HTTP_401_UNAUTHORIZED
    #         )


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        serializer.save(post=self.request.post_id)


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (GroupUserPermission, IsAuthenticated, )
