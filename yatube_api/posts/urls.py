from django.urls import include, path
from rest_framework.authtoken import views
from rest_framework.routers import SimpleRouter
from api.views import PostViewSet, CommentViewSet, GroupViewSet

app_name = 'posts'

router = SimpleRouter()

router.register('posts', PostViewSet)
router.register('groups', GroupViewSet)
router.register(r'posts/(?P<post_pk>\d)/comments', CommentViewSet, basename='comment')

urlpatterns = [
    path('api-token-auth/', views.obtain_auth_token),
]

urlpatterns += router.urls
