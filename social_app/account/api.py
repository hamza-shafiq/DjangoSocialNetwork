from rest_framework import generics
from rest_framework.response import Response
from .serializer import RegisterSerializer, UserSerializer
from .tasks import save_user_location
from django_q.tasks import async_task


class RegisterApi(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args,  **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        user_data = UserSerializer(user, context=self.get_serializer_context()).data

        # Run Async Task - Abstract API to fetch information
        async_task(save_user_location, user_data["id"])

        return Response({
            "user": user_data,
            "message": "User Created Successfully. Now perform Login to get your token",
        })
