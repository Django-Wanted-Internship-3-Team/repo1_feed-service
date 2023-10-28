from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from posts.models import HashTag, Post
from users.models import User


class StatisticsListViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.hasgtag = HashTag.objects.create(
            name="hashtag",
        )
        for i in range(1, 11):
            cls.users = User.objects.create_user(
                email=f"user{i}@example.com",
                username=f"username{i}",
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
            cls.posts.hashtag.set([cls.hasgtag])

    def setUp(self):
        pass
        # self.access_token = self.client.post(reverse("token_obtain_pair"), self.user_data).data["access"]

    def test_get_statistics_list_date_success(self):
        response = self.client.get(
            path=reverse("statistics"),
            data={
                "type": "date",
                "hashtag": "hashtag",
                "value": "count",
            },
            # HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_statistics_list_hour_success(self):
        response = self.client.get(
            path=reverse("statistics"),
            data={
                "type": "hour",
                "hashtag": "hashtag",
                "value": "count",
            },
            # HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_statistics_list_not_found(self):
        response = self.client.get(
            path=reverse("statistics"),
            data={
                "type": "date",
                "hashtag": "hashtag1",
                "value": "count",
            },
            # HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    # @TODO: 로그인 로직 구현 후 주석 풀기 @SaJH
    # def test_get_statistics_list_fail_unauthenticated(self):
    #     response = self.client.get(
    #         path=reverse("statistics"),
    #         data={
    #             "type": "date",
    #             "hashtag": "hashtag",
    #             "value": "count",
    #         },
    #     )
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_statistics_list_fail_missing_parameter(self):
        response = self.client.get(
            path=reverse("statistics"),
            data={
                "hashtag": "hashtag",
            },
            # HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_statistics_list_fail_invalid_parameter_type(self):
        response = self.client.get(
            path=reverse("statistics"),
            data={
                "type": "test",
                "hashtag": "hashtag",
                "value": "count",
            },
            # HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_statistics_list_fail_invalid_parameter_max_days(self):
        response = self.client.get(
            path=reverse("statistics"),
            data={
                "type": "date",
                "start": "2023-10-1",
                "end": "2023-11-10",
                "hashtag": "hashtag",
                "value": "count",
            },
            # HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_statistics_list_fail_invalid_parameter_value(self):
        response = self.client.get(
            path=reverse("statistics"),
            data={
                "type": "date",
                "hashtag": "hashtag",
                "value": "test",
            },
            # HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
