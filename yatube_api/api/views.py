from django.shortcuts import get_object_or_404
from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated

from posts.models import Comment, Group, Post
from .permissions import PostCommentUserPermission
from .serializers import CommentSerializer, GroupSerializer, PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (PostCommentUserPermission, IsAuthenticated)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (PostCommentUserPermission, IsAuthenticated)

    def get_queryset(self):
        post = get_object_or_404(Post, id=self.kwargs['post_pk'])
        return Comment.objects.filter(post=post.id)

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            post_id=int(self.kwargs.get('post_pk'))
        )


class GroupViewSet(mixins.RetrieveModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
