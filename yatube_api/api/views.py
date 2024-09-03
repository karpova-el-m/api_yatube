from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated

from posts.models import Comment, Group, Post
from .permissions import PostCommentUserPermission
from .serializers import CommentSerializer, GroupSerializer, PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated, PostCommentUserPermission)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated, PostCommentUserPermission)

    def get_queryset(self):
        return Comment.objects.filter(post=self.kwargs['post_pk'])

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
