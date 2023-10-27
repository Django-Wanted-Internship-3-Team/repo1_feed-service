from django.urls import reverse
from rest_framework.test import APIClient, APITestCase

from posts.models import Post
from users.models import User


class LikeAPITestCase(APITestCase):
    client = APIClient(enforce_csrf_checks=True)
    viewname = "likes"

    def setUp(self):
        self.user = User.objects.create(email="user")

        self.post = Post.objects.create(title="title", post_type="facebook", content="content")

    def test_post_without_auth(self):
        """logout and post like"""

        self.client.logout()

        response = self.client.post(
            path=reverse(
                viewname=self.viewname,
                kwargs={
                    "content_id": self.post.content_id,
                },
            ),
        )

        self.assertEqual(response.status_code, 401)

    def test_post_with_auth(self):
        """login and post like"""

        # self.client.force_login(self.user)
        self.client.force_authenticate(user=self.user)

        response = self.client.post(
            path=reverse(
                viewname=self.viewname,
                kwargs={
                    "content_id": self.post.content_id,
                },
            ),
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.post.like_count, Post.objects.first().like_count - 1)
