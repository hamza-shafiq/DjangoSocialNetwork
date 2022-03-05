from rest_framework.test import APITestCase, APIClient
from .models import Posts
from django.contrib.auth.models import User
from rest_framework import status


class PostTests(APITestCase):

    def setUp(self):
        # Create a test user instance
        self.client = APIClient()
        self.url = "/api/v1/social-app/post/"
        self.user = User.objects.create_superuser(
            username="Alex", password="Alpha@1234", email="alex@gmail.com",
            first_name="Alex", last_name="Hales"
        )
        self.post = Posts.objects.create(user=self.user, title="test post", content="test content")

    def test_create_new_post(self):
        """
        Ensure we can create a new post object.
        """
        new_post = {
            "user": self.user.id,
            "title": "another post",
            "content": "another post content"
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, new_post, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Posts.objects.count(), 2)

    def test_fetch_post(self):
        """
        Ensure we can fetch a post object.
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(dict(response.data[0])["title"], "test post")


class PostLikeDislikeTests(APITestCase):

    def setUp(self):
        # Create a test user instance
        self.client = APIClient()
        self.url = "/api/v1/social-app/like-dislike/"
        self.user = User.objects.create_superuser(
            username="Alex", password="Alpha@1234", email="alex@gmail.com",
            first_name="Alex", last_name="Hales"
        )
        self.post = Posts.objects.create(user=self.user, title="test post", content="test content")

    def test_create_new_post(self):
        """
        Ensure we can like / dislike a post.
        """
        post_like_dislike = {
            "user": self.user.id,
            "post": self.post.id,
            "likes": 1,
            "dislikes": 0
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, post_like_dislike, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["message"], "Post Liked / Disliked Successfully.")
