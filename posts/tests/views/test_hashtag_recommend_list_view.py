from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from posts.models import HashTag, Post
from users.models import User


class HashTagRecommendListViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.hasgtag1 = HashTag.objects.create(
            name="hashtag1",
        )
        cls.hasgtag2 = HashTag.objects.create(
            name="hashtag2",
        )
        for i in range(1, 10):
            cls.users = User.objects.create_user(
                email=f"user{i}@example.com",
                password="testpassword",
            )
            cls.posts = Post.objects.create(
                post_type="facebook",
                title=f"title {i}",
                content=f"content {i}",
                view_count=i,
                like_count=i,
                share_count=i,
                user=cls.users,
            )
            if i % 2 == 0:
                cls.posts.hashtag_set.set([cls.hasgtag2])
            else:
                cls.posts.hashtag_set.set([cls.hasgtag1, cls.hasgtag2])

    def setUp(self):
        pass
        # self.access_token = self.client.post(reverse("token_obtain_pair"), self.user_data).data["access"]

    def test_get_hash_tag_recommend_list_success(self):
        response = self.client.get(
            path=reverse("hashtag_recommend_list"),
            # HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEqual(response.data[0]["id"], 2)
        self.assertEqual(response.data[0]["name"], "hashtag2")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # @TODO: 로그인 로직 구현 후 주석 풀기 @SaJH
    # def test_get_hash_tag_recommend_list_fail_unauthenticated(self):
    #     response = self.client.get(
    #         path=reverse("hashtag_recommend_list"),
    #     )
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
