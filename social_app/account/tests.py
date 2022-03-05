from django.test import TestCase
from rest_framework.test import APITestCase, URLPatternsTestCase, APIRequestFactory
from django.contrib.auth.models import User
from rest_framework.test import force_authenticate
from .api import UserViewSet, RegisterApi
from rest_framework_simplejwt.views import TokenObtainPairView


class ViewSetTest(TestCase):

    def setUp(self):
        # Create a test user instance
        self.user = User.objects.create_superuser(
            username="Alex", password="Alpha@1234", email="alex@gmail.com",
            first_name="Alex", last_name="Hales"
        )

    def test_user_authentication(self):
        factory = APIRequestFactory()
        user = User.objects.get(username=self.user.username)
        view = UserViewSet.as_view(actions={'get': 'retrieve'})

        api_request = factory.get('')
        force_authenticate(api_request, user=user)
        response = view(api_request, pk=self.user.pk)

        self.assertEqual(response.status_code, 200)

    # def test_signup(self):
    #     factory = APIRequestFactory(enforce_csrf_checks=True)
    #     new_user = {
    #         "first_name": "Hamza",
    #         "last_name": "Shafique",
    #         "username": "Hamza",
    #         "password": "Alpha@1234",
    #         "email": "hamzashafique054@gmail.com",
    #     }
    #     register_view = RegisterApi.as_view()
    #     api_request = factory.post('register/', new_user, format='json')
    #     response = register_view(api_request)
    #
    #     self.assertEqual(response.status_code, 201)

    def test_login(self):
        factory = APIRequestFactory(enforce_csrf_checks=True)
        user_to_login = {
            "username": "Alex",
            "password": "Alpha@1234",
        }
        login_view = TokenObtainPairView.as_view()
        api_request = factory.post('login/', user_to_login, format='json')
        response = login_view(api_request)

        self.assertEqual(response.status_code, 200)

    def test_user_data(self):
        factory = APIRequestFactory(enforce_csrf_checks=True)
        user_view = UserViewSet.as_view(actions={'get': 'retrieve'})
        api_request = factory.get('')
        force_authenticate(api_request, user=self.user)
        response = user_view(api_request, pk=self.user.pk)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["username"], "Alex")
