from django.urls import include, path
from rest_framework.authtoken import views
from rest_framework.routers import SimpleRouter

from .views import CommentViewSet, GroupViewSet, PostViewSet

app_name = 'posts'

first_version_router = SimpleRouter()

first_version_router.register('v1/posts', PostViewSet)
first_version_router.register('v1/groups', GroupViewSet)
first_version_router.register(
    r'v1/posts/(?P<post_pk>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('v1/api-token-auth/', views.obtain_auth_token),
    path('', include(first_version_router.urls)),
]
