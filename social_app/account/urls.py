from django.urls import path, include

from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView, TokenVerifyView
)

from .api import RegisterApi, UserViewSet

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
      # Users
      path('', include(router.urls), name='users'),

      # Register new user
      path('register/', RegisterApi.as_view(), name='register'),

      # Login user to get refresh & access tokens
      path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

      # Refresh & verify access token
      path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
      path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
