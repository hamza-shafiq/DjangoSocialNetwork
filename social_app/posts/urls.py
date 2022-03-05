from .views import PostViewSet, PostLikeDislikeViewSet
from rest_framework.routers import DefaultRouter

app_name = "posts"

router = DefaultRouter()
router.register(r'post', PostViewSet, basename='post')
router.register(r'like-dislike', PostLikeDislikeViewSet, basename='like-dislike')
urlpatterns = router.urls
