from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from posts.models import Group, Post
from .permissions import IsAuthorOrReadOnly
from .serializers import CommentSerializer, GroupSerializer, PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели Post."""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated, IsAuthorOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели Comment."""
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated, IsAuthorOrReadOnly)

    def get_post(self):
        return get_object_or_404(Post, id=self.kwargs['post_pk'])

    def get_queryset(self):
        return self.get_post().comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            post_id=self.get_post().id
        )


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для модели Group."""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
