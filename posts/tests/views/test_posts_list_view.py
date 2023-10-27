import uuid

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from posts.models import HashTag, Post
from users.models import User


class PostListViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.hasgtag = HashTag.objects.create(
            name="hashtag",
        )
        for i in range(1, 6):
            cls.users = User.objects.create_user(
                email=f"user{i}@example.com",
                username=f"testuser{i}",
                password="testpassword",
            )
            cls.posts = Post.objects.create(
                content_id=uuid.uuid4(),
                post_type="facebook",
                title=f"title {i}",
                content=f"content {i}",
                view_count=i,
                like_count=i,
                share_count=i,
                user=cls.users,
                created_at=f"2023-10-1{i}",
                updated_at=f"2023-10-2{i}",
            )
            cls.posts = Post.objects.create(
                content_id=uuid.uuid4(),
                post_type="twitter",
                title=f"title {i}",
                content=f"content {i}",
                view_count=i,
                like_count=i,
                share_count=i,
                user=cls.users,
                created_at=f"2023-10-1{i}",
                updated_at=f"2023-10-2{i}",
            )
            cls.posts = Post.objects.create(
                content_id=uuid.uuid4(),
                post_type="instagram",
                title=f"title {i}",
                content=f"content {i}",
                view_count=i,
                like_count=i,
                share_count=i,
                user=cls.users,
                created_at=f"2023-10-1{i}",
                updated_at=f"2023-10-2{i}",
            )
            cls.posts = Post.objects.create(
                content_id=uuid.uuid4(),
                post_type="threads",
                title=f"title {i}",
                content=f"content {i}",
                view_count=i,
                like_count=i,
                share_count=i,
                user=cls.users,
                created_at=f"2023-10-1{i}",
                updated_at=f"2023-10-2{i}",
            )
            cls.posts.hashtag.set([cls.hasgtag])

    def setUp(self):
        pass
        # self.access_token = self.client.post(reverse("token_obtain_pair"), self.user_data).data["access"]

    def test_get_posts_list_success(self):
        response = self.client.get(
            path=reverse("list"),
            data={
                "type": "facebook",
                "hashtag": "hashtag",
            },
            # HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_filtered_post_list_facebook_success(self):
        response = self.client.get(
            path=reverse("list"),
            data={"type": "facebook", "hashtag": "hashtag", "title": "title 1", "content": "content 1"},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_filtered_post_list_twitter_success(self):
        response = self.client.get(
            path=reverse("list"),
            data={"type": "twitter", "hashtag": "hashtag", "title": "title 1", "content": "content 1"},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_filtered_post_list_instagram_success(self):
        response = self.client.get(
            path=reverse("list"),
            data={"type": "instagram", "hashtag": "hashtag", "title": "title 1", "content": "content 1"},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_filtered_post_list_threads_success(self):
        response = self.client.get(
            path=reverse("list"),
            data={"type": "threads", "hashtag": "hashtag", "title": "title 1", "content": "content 1"},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_posts_list_fail_invalid_parameter_type(self):
        response = self.client.get(
            path=reverse("list"),
            data={
                "type": "facebook1",
                "hashtag": "",
            },
            # HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
