from django.urls import path
from .views import PostViewSet
from rest_framework.routers import DefaultRouter

# from views import PostView
app_name = "posts"

router = DefaultRouter()
router.register(r'', PostViewSet, basename='post')
urlpatterns = router.urls

# urlpatterns = [
#     path('post/', PostViewSet, name='post'),
# ]
