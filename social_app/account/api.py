from rest_framework import generics, viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializer import RegisterSerializer, UserSerializer
from django.contrib.auth.models import User
from utils.abstarct_api import AbstractAPI

from .tasks import save_user_location
from django_q.tasks import async_task


class RegisterApi(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args,  **kwargs):
        # Validate email address through abstract-api
        abstract_api = AbstractAPI()
        valid_email = abstract_api.validate_email(email=request.data.get("email"))
        if not valid_email["is_valid_format"]:
            content = {'message': 'invalid email address!'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        # Create new user record
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user_data = UserSerializer(user, context=self.get_serializer_context()).data

        # Run Async Task - Abstract API to fetch information
        async_task(save_user_location, user_data["id"])

        content = {
            "data": user_data,
            "message": "User Created Successfully. Now perform Login to get your token"
        }
        return Response(content, status=status.HTTP_201_CREATED)


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer
